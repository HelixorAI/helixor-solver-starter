import { readFile, writeFile } from 'node:fs/promises';

const baseUrl = process.env.SOLVER_URL?.replace(/\/+$/, '');
const token = process.env.SOLVER_TOKEN;
if (!baseUrl || !token || baseUrl.includes('replace-with-')) {
  console.error('Set SOLVER_URL and SOLVER_TOKEN in .env (see README).');
  process.exit(1);
}

const request = JSON.parse(await readFile('data/container-logistics-request.json', 'utf8'));
const headers = { Authorization: `Bearer ${token}` };

async function check(response, action) {
  if (!response.ok) {
    const body = await response.text();
    throw new Error(`${action} failed (${response.status}): ${body}`);
  }
  return response.json();
}

try {
  const manifest = await check(
    await fetch(`${baseUrl}/api/v1/manifests/${request.problem_type}`, { headers }),
    'Manifest lookup',
  );
  console.log(`Using manifest: ${manifest.problem_type ?? request.problem_type}`);

  const result = await check(
    await fetch(`${baseUrl}/api/v1/solve/${request.problem_type}`, {
      method: 'POST',
      headers: { ...headers, 'Content-Type': 'application/json' },
      body: JSON.stringify(request),
    }),
    'Solve',
  );
  await writeFile('solve-result.json', `${JSON.stringify(result, null, 2)}\n`);
  console.log(JSON.stringify(result, null, 2));
  if (result.solution?.admission?.is_feasible !== true) {
    console.error('The API returned, but the final plan did not carry feasible admission evidence.');
    process.exitCode = 2;
  } else {
    console.log('Final plan includes feasibility evidence.');
  }
} catch (error) {
  console.error(error.message);
  process.exitCode = 1;
}
