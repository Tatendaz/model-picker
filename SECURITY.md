# Security

Do not include API keys, private prompts, or session files in public issues.
Report vulnerabilities privately through GitHub's security advisory feature when
available, or contact the maintainer through their GitHub profile.

Model Picker sends bounded prompt excerpts to TypeSafe when checks run. Read the
README's data-sharing section before trusting the hook. It never switches the
active model or reads repository source files. Credentials are loaded at runtime.
