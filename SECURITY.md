# Security Policy

## Scope

IFRS-AI Inspector is a research prototype. Security reports should concern repository code, dependency handling, data exposure, unsafe defaults, or workflows that could lead to unauthorized access or disclosure.

## Reporting

Please do not publish credentials, private keys, access tokens, confidential client information, restricted standards content, or exploitable security details in a public issue. Use GitHub's private security-reporting mechanisms where available, or contact the repository owner through an appropriate private channel.

## Data handling

- Do not commit secrets or credentials.
- Do not commit confidential audit/client data.
- Do not upload restricted professional standards content unless you have the necessary rights.
- Use synthetic, public, or appropriately licensed data for public demonstrations.
- Treat model prompts, outputs, embeddings, logs, and vector stores as potentially sensitive when they contain source material.

## Production boundary

No security assurance, certification, or production-readiness claim is made for this repository. Real deployments require independent security, privacy, legal, model-risk, and professional review.
