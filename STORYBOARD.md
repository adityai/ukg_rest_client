# Storyboard
Here’s a chronological breakdown of how I built this UKG REST API client and the associated union leave workflow:

1) Bootstrapped the client against the mock UKG API

- I started by generating a mock UKG HR Service Delivery REST API from the public v2 spec so I could develop without access to a real UKG tenant.
- Once the mock service existed under mock_ukg_rest, I added ukg_api_client.py on top of it and wired in the first “vacation request and approval” flow, so I could prove end‑to‑end request/response handling against the mock API.
- I added a requirements.txt file so the project could be installed consistently on any machine.

2) Added testing and basic tooling

- After I had the initial client and vacation workflow working, I added pytest and an initial test file so I could run automated tests locally and validate behavior as I iterated.
- I then added more payroll‑oriented endpoints and sample data into the mock services (payroll runs and pay stubs), and extended ukg_api_client.py to support creating payroll runs and pay stubs through the same client abstraction.
- To make the client easier to configure across environments, I externalized all authentication details (app ID, secret, client ID, company short name, base URL) into environment variables instead of hard‑coding them.
- I simplified how request/response handling worked in ukg_api_client.py, refactoring down to a single make_request helper and then updated all existing client methods to go through that one code path.

3) Hardened the client and test suite

- Once the basic flows were stable, I added more unit tests (with help from Amazon Q to scaffold some of them) to expand coverage, including happy‑path and error‑handling scenarios.
- When a couple of tests were noisy while I was refactoring, I temporarily commented them out so I could keep the pipeline green while I iterated.
- I introduced setup.py and a .circleci pipeline so the client could be packaged as a Python module and built/tested automatically on every commit in CI.
- I then fixed and tuned the CircleCI config, and added a build‑status badge to the README. After that, I adjusted the badge so it would show status for any branch, not just main.

4) Expanded functional coverage: payroll, employees, and org

- With the infrastructure in place, I extended the client to cover more HR and payroll scenarios:
    - Added methods and mock data for creating deductions and taxes, plus endpoints to retrieve them.
    - Added support for employees and organizational structures (employees, departments, org methods) on the client, and wired corresponding endpoints in the mock server.
- I continued to refine the README during this period so it clearly explained what the client does, how to configure it, and how to run the tests and demos.

5) Built the external union entitlements and compliance data layer

- Once the core UKG flows were in place, I focused on the gap the real UKG APIs don’t cover: union entitlements and compliance rules.
- I designed a small external SQLite database (union_entitlements.db) under external_data with tables for unions, union_members, entitlements, and member_entitlements, and then populated it with sample union and compliance data.
- On top of that database I added union_entitlements_service.py so my workflow code could query union memberships and entitlements through a simple service abstraction instead of talking to the database directly.
- I updated .gitignore so the generated data artifacts wouldn’t accidentally be committed.

6) Implemented richer employee/org methods and laid groundwork for the union workflow

- I added more detailed employee and organization methods in ukg_api_client.py to retrieve the contextual data needed for union scenarios (employee profile, org info, etc.).
- I then created scaffolding for union_leave_workflow.py: a script dedicated to implementing the “union leave” use case end‑to‑end, but initially just with structure and placeholders for the steps.

7) Completed the full union leave workflow

- With the scaffolding ready and the union/compliance data layer in place, I implemented the full “Union Leave Request Workflow”:
    - Create a time‑off request for a union member through the UKG REST client.
    - Look up the member’s union and entitlements from the external SQLite database via union_entitlements_service.py.
    - Verify the employee’s accrual balance using the UKG REST mock APIs.
    - Evaluate compliance parameters (also stored in external_data) to ensure the request doesn’t violate rules.
    - Either approve the request (and reflect that in UKG) or reject it with a clear reason.
- I also updated ukg_api_client.py where needed to support this workflow end‑to‑end, and committed those changes as “Complete union_leave_workflow”.

8) Polished the demo and documentation

- Once the core workflow logic was solid, I refined the union_leave_workflow.py output to be visually appealing and easy to follow in a demo setting (clear steps, color/formatting, and readable messages).
- I added RUN_DEMO.md to give a simple, copy‑paste set of instructions for:
    - Starting the mock UKG server
    - Running the REST client
    - Running the union leave workflow end‑to‑end.
- I iterated on README.md several times to clarify the developer’s disclosure, describe which parts of the repo were generated vs. handwritten, document the external union entitlement/compliance database, and explain how to run everything locally or point the client at real UKG Pro environments.
- Finally, I merged the develop branch back into main via pull requests (#5, #6, #7) so all the incremental changes—tests, CI, payroll features, employee/org methods, union data layer, and the union leave workflow—were integrated into a clean main branch.

