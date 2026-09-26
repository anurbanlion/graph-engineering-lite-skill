# Preguntas Frecuentes — Gantt Diagram

The dates below are logical, uniform-duration execution slots rather than estimates. Each Gantt task is one target-area instance of a dependency-diagram worker responsibility. Therefore, a Worker 2 task includes both its fixture and Storybook substeps; they MUST NOT be scheduled as separate Worker 2 tasks for the same organism.

`done` tasks are recorded history and render with Mermaid's completed-task color.

When one persistent worker is already assigned in a time unit, an eligible task from the next dependency layer MAY fill the second slot with a different worker. This is why W4 begins HeroBannerSearch analytics in T5 while W3 continues its sequential QuestionsAndAnswers and ContactCard implementations.

```mermaid
gantt
    title Complete execution plan — 25 tasks across organisms
    dateFormat  YYYY-MM-DD
    axisFormat  %d

    section Independent
    T1 — W6 Route shell                              :done, routeShell, 2026-09-22, 1d

    section HeroBannerSearch
    T1 — W1 Props and propsEngine                    :done, heroProps, 2026-09-22, 1d
    T2 — W2 Fixtures and Storybook                   :done, heroFixturesAndStories, 2026-09-23, 1d
    T4 — W3 Flat organism and styles                 :done, heroOrganism, 2026-09-25, 1d
    T5 — W4 Analytics                                :done, heroAnalytics, 2026-09-26, 1d
    T7 — W5 Publication                              :done, heroPublication, 2026-09-28, 1d
    T8 — W7 Journey integration                      :done, heroIntegration, 2026-09-29, 1d
    T10 — W8 Atoms and molecules                     :done, heroAtomsAndMolecules, 2026-10-01, 1d
    T11 — W9 Atoms and molecules Storybook           :done, heroAtomsAndMoleculesStories, 2026-10-02, 1d

    section QuestionsAndAnswers
    T2 — W1 Props and propsEngine                    :done, questionsProps, 2026-09-23, 1d
    T3 — W2 Fixtures and Storybook                   :done, questionsFixturesAndStories, 2026-09-24, 1d
    T5 — W3 Flat organism and styles                 :done, questionsOrganism, 2026-09-26, 1d
    T6 — W4 Analytics                                :done, questionsAnalytics, 2026-09-27, 1d
    T8 — W5 Publication                              :done, questionsPublication, 2026-09-29, 1d
    T9 — W7 Journey integration                      :done, questionsIntegration, 2026-09-30, 1d
    T11 — W8 Atoms and molecules                     :done, questionsAtomsAndMolecules, 2026-10-02, 1d
    T12 — W9 Atoms and molecules Storybook           :done, questionsAtomsAndMoleculesStories, 2026-10-03, 1d

    section ContactCard
    T3 — W1 Props and propsEngine                    :done, contactProps, 2026-09-24, 1d
    T4 — W2 Fixtures and Storybook                   :done, contactFixturesAndStories, 2026-09-25, 1d
    T6 — W3 Flat organism and styles                 :done, contactOrganism, 2026-09-27, 1d
    T7 — W4 Analytics                                :done, contactAnalytics, 2026-09-28, 1d
    T9 — W5 Publication                              :done, contactPublication, 2026-09-30, 1d
    T10 — W7 Journey integration                     :done, contactIntegration, 2026-10-01, 1d
    T12 — W8 Atoms and molecules                     :done, contactAtomsAndMolecules, 2026-10-03, 1d
    T13 — W9 Atoms and molecules Storybook           :done, contactAtomsAndMoleculesStories, 2026-10-04, 1d
```

T13 has one task because the ContactCard W9 instance is the final eligible task; no second task remains without duplicating the persistent W9 worker.
