Feature: Resolve a Graph Engineering job
  The runtime selects one job from the project's local job store or from its
  selected Graph Engineering skill.

  Background:
    Given a project root supplied by the caller
    And an optional skill root supplied by the caller, otherwise derived from resolve_job.py

  Rule: Validate job identifier

    Scenario: Identifier is valid
      Given an identifier in kebab-case without path separators
      When resolve_job is called with that identifier
      Then it continues with job resolution

    Scenario: Identifier is invalid
      Given an invalid job identifier
      When resolve_job is called with that identifier
      Then it fails before searching for a job

      Examples:
        | category       | identifier         |
        | empty          | ""                 |
        | Unix path      | "group/design"     |
        | Windows path   | "group\\design"   |
        | traversal      | "."                |
        | traversal      | ".."               |
        | invalid format | "Design-Job"       |
        | invalid format | "design_job"       |
        | invalid format | "design job"       |
        | invalid format | "design--job"      |

  Rule: Discover local job
    The local job folder path is exactly
    project_root/.graph-engineering/local/jobs/<job-name>.

    Scenario: Local job exists exactly
      Given the exact local job folder path for <job-identifier> exists
      When the local job is discovered for that identifier
      Then it returns that local job folder path

      Examples:
        | job identifier | local job folder path                                        |
        | design-job     | project_root/.graph-engineering/local/jobs/design-job        |
        | stage-job      | project_root/.graph-engineering/local/jobs/stage-job         |

    Scenario: Local job does not exist
      Given the exact local job folder path for <job-identifier> does not exist
      When the local job is discovered for that identifier
      Then it returns no local job folder path

      Examples:
        | job identifier | expected local job folder path                               |
        | design-job     | project_root/.graph-engineering/local/jobs/design-job        |
        | stage-job      | project_root/.graph-engineering/local/jobs/stage-job         |

  Rule: Discover skill jobs

    Scenario: Exactly one skill job exists
      Given exactly one job folder matching <job-identifier> exists under skill_root/jobs/**
      When skill jobs are discovered for that identifier
      Then it returns that skill job folder path

      Examples:
        | job identifier | skill job folder path                                      |
        | design-job     | skill_root/jobs/design-job                                 |
        | design-job     | skill_root/jobs/(authoring)/design-job                     |
        | stage-job      | skill_root/jobs/(workflow)/(testing)/stage-job             |

    Scenario: No skill job exists
      Given no job folder matching <job-identifier> exists under skill_root/jobs/**
      When skill jobs are discovered for that identifier
      Then it returns no skill job folder path

      Examples:
        | job identifier |
        | design-job     |
        | stage-job      |

    Scenario: Two or more skill jobs exist
      Given two or more job folders matching <job-identifier> exist under skill_root/jobs/**
      When skill jobs are discovered for that identifier
      Then it fails with an ambiguity error
      And it includes every conflicting skill job folder path

      Examples:
        | job identifier | job_md_path                                       | source | resolution            |
        | design-job     | skill_root/jobs/design-job/JOB.md                 | skill  | ambiguity error       |
        | design-job     | skill_root/jobs/(authoring)/design-job/JOB.md     | skill  | ambiguity error       |
        | stage-job      | skill_root/jobs/(workflow)/stage-job/JOB.md       | skill  | ambiguity error       |
        | stage-job      | skill_root/jobs/(testing)/stage-job/JOB.md        | skill  | ambiguity error       |

  Rule: Validate job definition
    A candidate job folder path is valid only when its folder contains JOB.md.
    GRAPH.json and a scripts directory are optional job resources; neither
    replaces JOB.md.

    Scenario: Candidate job folder path has JOB.md
      Given a local or skill job folder path contains JOB.md
      When its job definition is validated
      Then the job folder path is valid

    Scenario: Candidate job folder path does not have JOB.md
      Given a local or skill job folder path does not contain JOB.md
      When its job definition is validated
      Then it fails that the job definition is invalid

  Rule: Prioritize local job

    Scenario: Valid local job exists and no skill job exists
      Given a valid local job exists for <job-identifier>
      And no valid skill job exists for that identifier
      When resolve_job is called with that identifier
      Then it returns the local job folder path
      And its source is "local"

      Examples:
        | job identifier | job_md_path                                              | source | resolution |
        | my-job         | project_root/.graph-engineering/local/jobs/my-job/JOB.md | local  | returned   |

    Scenario: Valid skill job exists and no local job exists
      Given a valid skill job exists for <job-identifier>
      And no local job exists for that identifier
      When resolve_job is called with that identifier
      Then it returns the skill job folder path
      And its source is "skill"

      Examples:
        | job identifier | job_md_path                                   | source | resolution |
        | my-job         | skill_root/jobs/(authoring)/my-job/JOB.md     | skill  | returned   |

    Scenario: Valid local and skill jobs both exist
      Given a valid local job and a valid skill job exist for <job-identifier>
      When resolve_job is called with that identifier
      Then it returns the local job folder path as a testing override
      And its source is "local"

      Examples:
        | job identifier | job_md_path                                              | source | resolution   |
        | my-job         | project_root/.graph-engineering/local/jobs/my-job/JOB.md | local  | returned     |
        | my-job         | skill_root/jobs/(authoring)/my-job/JOB.md                | skill  | not returned |

    Scenario: Local candidate is invalid and skill job is valid
      Given a local job exists without JOB.md for <job-identifier>
      And a valid skill job exists for that identifier
      When resolve_job is called with that identifier
      Then it fails that the local job definition is invalid
      And it does not return the skill job

      Examples:
        | job identifier | job_md_path                                                        | source | resolution   |
        | my-job         | project_root/.graph-engineering/local/jobs/my-job/JOB.md (missing) | local  | invalid      |
        | my-job         | skill_root/jobs/(authoring)/my-job/JOB.md                          | skill  | not returned |

  Rule: Resolve job

    Scenario: A job is resolved
      Given identifier, discovery, definition validation, and priority succeed for <job-identifier>
      When resolve_job is called with <job-identifier>
      Then it returns the selected ResolvedJob

      Examples:
        | field               | value                                                            |
        | identifier          | my-job                                                           |
        | job_folder_path     | project_root/.graph-engineering/local/jobs/my-job               |
        | source              | local                                                            |
        | job_md_path         | project_root/.graph-engineering/local/jobs/my-job/JOB.md        |
        | graph_json_path     | project_root/.graph-engineering/local/jobs/my-job/GRAPH.json    |
        | scripts_folder_path | project_root/.graph-engineering/local/jobs/my-job/scripts       |

    Scenario: No job is resolved
      Given no local job folder path exists
      And no skill job folder path exists
      When resolve_job is called with "design-job"
      Then it fails that the job was not found
