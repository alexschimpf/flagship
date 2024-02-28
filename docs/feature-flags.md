# Feature Flags

Feature flags allow you to enable or disable features/functionality at runtime. They enable the gradual rollout of
features, continuous deployment, A/B testing, quick rollbacks, and dark launches.

In Flagship, each feature flag is given a name, description, and conditions, and can also be toggled on and off. If a
feature flag is enabled but is given no conditions, it is essentially enabled for all. The name of each feature flag
is its primary identifier. It is recommended to follow a consistent naming convention, e.g. lower or upper snake case.

<hr>

## Conditions

<p>
    Conditions allow you to control when feature flags are enabled. Before setting feature flag conditions, you should
    first create one or more <a href="/flagship/context-fields">context fields</a>. You can then build your conditions based off
    these. There are different operators that can be used based on the value type of a context field. Conditions can be
    joined together using AND/OR boolean operators to form more complex conditions.
</p>

<hr>

## Audit Logs

<p>
    All changes made to feature flags are recorded and can be viewed in the UI. You can see which users changed which
    fields and at what time.
</p>
