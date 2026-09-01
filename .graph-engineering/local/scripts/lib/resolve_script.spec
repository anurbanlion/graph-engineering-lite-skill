Feature: Resolve a Graph Engineering Python script
  The runtime selects one eligible Python script from the project's local
  script stores or from its selected Graph Engineering skill.

  Background:
    Given a project root supplied by the caller
    And an optional skill root supplied by the caller, otherwise derived from resolve_script.py

  Rule: Validate script identifier

    Scenario: Identifier is valid
      Given a lowercase snake_case script identifier that starts with a letter
      And the identifier has no path separators or `.py` extension
      When resolve_script is called with that identifier
      Then it continues with script resolution

      Examples:
        | script identifier              |
        | prepare                        |
        | read_job_inputs                |
        | compile_initiatives_tasks      |
        | version2                       |
        | version2_task3                 |

    Scenario: Identifier is invalid
      Given an invalid script identifier
      When resolve_script is called with that identifier
      Then it fails before searching for a script

      Examples:
        | category         | script identifier    |
        | empty            | ""                   |
        | Unix path        | "nested/prepare"     |
        | Windows path     | "nested\\prepare"   |
        | traversal        | "."                  |
        | traversal        | ".."                 |
        | Python extension | "prepare.py"         |
        | kebab-case       | "read-job-inputs"    |
        | uppercase        | "ReadJobInputs"      |
        | whitespace       | "read job inputs"    |
        | leading digit    | "2read_inputs"       |
        | repeated underscore | "read__inputs"    |
        | leading underscore  | "_read_inputs"    |
        | trailing underscore | "read_inputs_"    |

  Rule: Discover local scripts
    Eligible local scripts are `.py` files outside `__pycache__`, found under
    project_root/.graph-engineering/local/scripts/** or under
    project_root/.graph-engineering/local/jobs/<job-identifier>/scripts/**.

    Scenario: Exactly one local script exists
      Given exactly one local script file path matching <script-identifier>.py exists
      When local scripts are discovered for <script-identifier>
      Then it returns that local script file path

      Examples:
        | script identifier | script_path                                                                     | scope  |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.py                        | shared |
        | prepare           | project_root/.graph-engineering/local/jobs/my-job/scripts/prepare.py            | job    |
        | prepare           | project_root/.graph-engineering/local/jobs/my-job/scripts/helpers/prepare.py    | job    |

    Scenario: No local script exists
      Given no eligible local script file path matching <script-identifier>.py exists
      When local scripts are discovered for <script-identifier>
      Then it returns no local script file path

      Examples:
        | script identifier |
        | prepare           |
        | compile_api       |

    Scenario: Two or more local scripts exist
      Given two or more eligible local script file paths matching <script-identifier>.py exist
      When local scripts are discovered for <script-identifier>
      Then it fails with an ambiguity error
      And it includes every conflicting local script file path

      Examples:
        | script identifier | script_path                                                                  | source | scope  | resolution      |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.py                     | local  | shared | ambiguity error |
        | prepare           | project_root/.graph-engineering/local/jobs/my-job/scripts/prepare.py         | local  | job    | ambiguity error |

    Scenario: Ineligible local files are ignored
      Given no eligible local script file path matching <script-identifier>.py exists
      When local scripts are discovered for <script-identifier>
      Then it returns no local script file path

      Examples:
        | script identifier | ineligible path                                                                |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.txt                      |
        | prepare           | project_root/.graph-engineering/local/scripts/__pycache__/prepare.py           |

  Rule: Discover skill scripts
    Eligible skill scripts are `.py` files outside `__pycache__`, found under
    skill_root/scripts/** or under skill_root/jobs/**/scripts/**.

    Scenario: Exactly one skill script exists
      Given exactly one skill script file path matching <script-identifier>.py exists
      When skill scripts are discovered for <script-identifier>
      Then it returns that skill script file path

      Examples:
        | script identifier | script_path                                                    | scope  |
        | prepare           | skill_root/scripts/prepare.py                                  | shared |
        | prepare           | skill_root/jobs/my-job/scripts/prepare.py                      | job    |
        | prepare           | skill_root/jobs/(authoring)/my-job/scripts/helpers/prepare.py  | job    |

    Scenario: No skill script exists
      Given no eligible skill script file path matching <script-identifier>.py exists
      When skill scripts are discovered for <script-identifier>
      Then it returns no skill script file path

      Examples:
        | script identifier |
        | prepare           |
        | compile_api       |

    Scenario: Two or more skill scripts exist
      Given two or more eligible skill script file paths matching <script-identifier>.py exist
      When skill scripts are discovered for <script-identifier>
      Then it fails with an ambiguity error
      And it includes every conflicting skill script file path

      Examples:
        | script identifier | script_path                                              | source | scope  | resolution      |
        | prepare           | skill_root/scripts/prepare.py                            | skill  | shared | ambiguity error |
        | prepare           | skill_root/jobs/(authoring)/my-job/scripts/prepare.py    | skill  | job    | ambiguity error |

    Scenario: Ineligible skill files are ignored
      Given no eligible skill script file path matching <script-identifier>.py exists
      When skill scripts are discovered for <script-identifier>
      Then it returns no skill script file path

      Examples:
        | script identifier | ineligible path                                        |
        | prepare           | skill_root/scripts/prepare.json                        |
        | prepare           | skill_root/scripts/__pycache__/prepare.py              |
        | prepare           | skill_root/jobs/my-job/prepare.py                      |

  Rule: Prioritize local script

    Scenario: Valid local script exists and no skill script exists
      Given a unique eligible local script exists for <script-identifier>
      And no eligible skill script exists for <script-identifier>
      When resolve_script is called with <script-identifier>
      Then it returns the local script file path
      And its source is "local"

      Examples:
        | script identifier | script_path                                                  | source | scope  | resolution |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.py     | local  | shared | returned   |

    Scenario: Valid skill script exists and no local script exists
      Given a unique eligible skill script exists for <script-identifier>
      And no eligible local script exists for <script-identifier>
      When resolve_script is called with <script-identifier>
      Then it returns the skill script file path
      And its source is "skill"

      Examples:
        | script identifier | script_path                                         | source | scope | resolution |
        | prepare           | skill_root/jobs/(authoring)/my-job/scripts/prepare.py | skill | job   | returned   |

    Scenario: Valid local and skill scripts both exist
      Given a unique eligible local script and a unique eligible skill script exist for <script-identifier>
      When resolve_script is called with <script-identifier>
      Then it returns the local script file path as an override
      And its source is "local"

      Examples:
        | script identifier | script_path                                                  | source | scope  | resolution   |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.py     | local  | shared | returned     |
        | prepare           | skill_root/jobs/(authoring)/my-job/scripts/prepare.py        | skill  | job    | not returned |

    Scenario: Local scripts are ambiguous and a skill script is valid
      Given two or more eligible local script file paths exist for <script-identifier>
      And a unique eligible skill script exists for <script-identifier>
      When resolve_script is called with <script-identifier>
      Then it fails with a local ambiguity error
      And it does not return the skill script

      Examples:
        | script identifier | script_path                                                                  | source | scope  | resolution      |
        | prepare           | project_root/.graph-engineering/local/scripts/prepare.py                     | local  | shared | ambiguity error |
        | prepare           | project_root/.graph-engineering/local/jobs/my-job/scripts/prepare.py         | local  | job    | ambiguity error |
        | prepare           | skill_root/jobs/(authoring)/my-job/scripts/prepare.py                        | skill  | job    | not returned    |

  Rule: Resolve script

    Scenario: A script is resolved
      Given identifier, discovery, and priority succeed for <script-identifier>
      When resolve_script is called with <script-identifier>
      Then it returns the selected ResolvedScript

      Examples:
        | field             | value                                                        |
        | identifier        | prepare                                                      |
        | script_path       | project_root/.graph-engineering/local/scripts/prepare.py    |
        | source            | local                                                        |
        | scope             | shared                                                       |

    Scenario: No script is resolved
      Given no local script file path exists
      And no skill script file path exists
      When resolve_script is called with <script-identifier>
      Then it fails that the script was not found
