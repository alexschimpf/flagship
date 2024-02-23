# Context Fields

<p>
A context field exists within a single project.
Context fields describe the context when resolving which feature flags are enabled.
For example, suppose you have a website that you want to control with feature flags.
When you ask the Flagship API to determine which feature flags are enabled for the current user, you need to describe
the user to Flagship. So you may do this by providing the following context fields to Flagship: `user_id`` and `country_code`.
You would create a separate context field for each and tell Flagship their types (i.e. integer and string).
You can then use these context fields in your feature flag conditions. For example, you could have conditions like:
```
(
    `user_id` is one of [1,2,3] AND
    `country_code` is not "US"
) OR
(
    `country_code` is "US"
)
```
Context fields can be assigned the following types: integer, number, string, boolean, semantic version, integer list, string list, and enum list.
</p>

<hr>

## Field Keys

<p>
Field keys are the actual keys you plan to pass to the Flags API. For example if your context includes a user ID, you
could have a context field with field key `user_id`. This cannot be changed after a context field is created.
</p>
<p>
In other words, field keys are only referenced by the Flags API, whereas the context field name is only relevant within the
Flagship UI.
</p>

<hr>

## Value Types

A context field's value type describes what type of value it is expected to hold.
For example, if you have a context field for a user's email address, it would have a "string" (i.e. text) value type.
This cannot be changed after a context field is created.

### Integer

Used for integers (e.g. 123).
<br>
Operators inlude:

- IS, IS NOT
- IS ONE OF
- IS NOT ONE OF
- &lt;
- &lt;=
- &gt;
- &gt;=

### Number

Used for floating point numbers (e.g. 1.23).
<br>
Operators are the same as for Integer.

### String

For text values (e.g. "US").
<br>
Operators include:

- IS
- IS NOT
- MATCHES
- IS ONE OF
- IS NOT ONE OF

### Boolean

For boolean values (e.g. true and false).
<br>
Operator include:

- IS
- IS NOT

### Semantic Version

For semantic version strings (e.g. 1.2.3).
<br>
Operators include:

- IS
- IS NOT
- &lt;
- &lt;=
- &gt;
- &gt;=

### Enum

<p>
Enums are named strings or integers.
For example, suppose your users can be assigned to one or more based groups, and these groups are identified by unique integer IDs.
When you are configuring your feature flag conditions, you want the conditions to be as human friendly as possible.
It may be confusing for someone to see conditions like:
```
`groups` HAS ONE OF [3, 4]
```

What is group 3? What is group 4?
</p>
<p>
A way to improve on this is to use the enum value type for the `groups` context field.
When you assign a context field to the enum value type, you must also define an <i>Enum Definition</i>.
The enum definition should be a single-level JSON blob, where keys are strings and values are either all strings or all integer.
The JSON keys represent the human-friendly enum names, whereas the values represent the values meant to be passed to the Flags API.
So you may have something like this for your `groups` enum definition:
```
{
    "Read Only": 1,
    "Standard": 2,
    "Admin": 3,
    "Owner": 4
}
```
</p>

So now feature flag conditions will appear in the Flagship UI like so:
```
`groups` HAS ONE OF ["Admin", "Owner"]
```

### Integer List

For lists containing only integers (e.g. [1, 2, 3]).
<br>
Operators include:

- HAS
- DOES NOT HAVE
- HAS ONE OF
- DOES NOT HAVE ONE OF

### String List

For lists containing only strings (e.g. ["a", "b", "c"]).
<br>
Operators include:

- HAS
- DOES NOT HAVE
- HAS ONE OF
- DOES NOT HAVE ONE OF

### Enum List

For lists containing only enums. Enums are described above.
<br>
Operators include:

- HAS
- DOES NOT HAVE
- HAS ONE OF
- DOES NOT HAVE ONE OF
