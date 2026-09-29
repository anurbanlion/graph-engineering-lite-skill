- Organisms are exported by `src/shared/components/organisms/index.ts`.
- Organisms exist under folder `src/shared/components/organisms/<organism>/`.
- Organisms are composed of several files, including:

src/shared/components/organisms/[component-name]
|-- [component-name].component.tsx // implementation
|-- [component-name].module.scss // styles
|-- [component-name].props.ts // component contract and auxiliary types (ex. analytics context types)
|-- [component-name].fixtures.ts // mock data
|-- [component-name].stories.tsx // storybook stories
|-- index.ts

- Atoms, molecules and organism must only use @shared/ utilities, if they reference something outside it must be changed or the utility/componente, etc must be migrated

- After making or reviewing repository changes, the orchestrator and workers MUST run `git -c core.autocrlf=false -c core.whitespace=cr-at-eol diff --check` instead of plain `git diff --check` to avoid line-ending conversion warnings and false trailing-whitespace reports.

- Workers MUST invoke required binaries directly. Do not wrap commands in `bash -lc` or another shell launcher unless the task specifically requires shell-only syntax.

- Links to workspace files MUST use the UNC path with forward slashes, beginning with `//wsl.localhost/Ubuntu-26.04/`, and wrap the link target in angle brackets. Example: `[RULES.md](<//wsl.localhost/Ubuntu-26.04/home/user/projects/chikiarena-main/.loop/artifacts/RULES.md>)`.

- When a component needs related navigation destinations, it MUST receive them as a typed `routes` object keyed by destination (for example, `{ catalog: Route; product: Route }`), not as separate href props.
