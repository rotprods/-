// Recipe for functions.exec; tools are supplied by Work Mode, not a global Node service.
// Invoke from the orchestrator. Coverage only includes calls made through this function.
async function observedCall(tools, toolName, args, root, runId) {
  const start = Date.now();
  let result, status;
  try { result = await tools[toolName](args); status = result.isError ? 'error' : 'returned'; }
  catch (error) { status = 'exception'; result = {isError: true, error: String(error)}; }
  const safe = x => "'" + x.replaceAll("'", "'\\''") + "'";
  const cmd = 'python3 tools/record_connector.py --tool ' + safe(toolName) + ' --run ' + safe(runId) + ' --status ' + status + ' --duration-ms ' + (Date.now()-start);
  const logged = await tools.exec_command({cmd,workdir:root,max_output_tokens:100});
  if (logged.exit_code !== 0) throw new Error('Telemetry write failed; reconcile provider result before retrying');
  return result;
}
