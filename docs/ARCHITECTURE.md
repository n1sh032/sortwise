# Architecture and development

UI: `web/` contains the folder selection and activity presentation. Transport: `src/web_runtime.py` validates browser requests and schedules one operation at a time. Application: `src/web.py` validates paths and invokes the existing sorting service. Domain behavior: `src/sorter.py` owns readiness, classification and safe moves. `src/logger.py` owns the CSV record.

Run `python src/web.py --folder "C:\\path\\to\\folder"` for the dashboard. It prints `http://sortwise.localhost:8012`. `SORTWISE_FOLDER` sets the default for both entry points. CLI watcher and browser operations should use separate folders if run simultaneously. The model-assisted audit and training experiment remain optional.

## Engineering conventions

Each repository is independently runnable. Presentation calls a transport adapter, which invokes application behavior. I/O stays at explicit boundaries so tests can replace external providers. Long browser operations have one owner, reject overlapping requests, and report success or failure through the UI. Relay uses async provider requests; video and desktop work use a worker or an existing sequential CLI loop.

New behavior should validate input before touching a user's files or desktop, report partial failures accurately, and have a regression test for a concrete failure mode. Run the repository's checks before committing and document the exact manual checks separately from mocked tests.

The local apps share a request/status pattern, accessible form controls, and a responsive layout. Small standard-library transports are kept inside each repository so they do not require a sixth repository at runtime. The matching transport modules should be updated together when changing that contract.

## Local addresses

The browser resolves `.localhost` names to the loopback interface. These addresses are scoped to this computer. Start the Python process before opening the address. Chrome and Edge support this setup. A distinct port lets each project run alongside the others without an OS hosts-file change.

## Evaluation

Automated checks verify the workflows represented by their fixtures. Real model access, physical microphones and desktop focus still need environment-specific checks. CI is included under `.github/workflows/checks.yml`; its remote result must be checked after pushing.

Remaining work should be driven by observations from real use. Dataset accuracy, provider access and desktop-device behavior cannot be established by a successful test run alone.

## Verification for this change

7 tests passed. Chrome loaded the branded address at desktop and phone widths. A selected scratch file was sorted and its move result appeared in Activity. Full CLIP/PDF classification accuracy and the correction-trained experiment remain unmeasured.
