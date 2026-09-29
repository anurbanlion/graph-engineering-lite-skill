Feature: Product Search
The user can discover and locate catalog products through the search engine.

## Rules

- [x] While the user types more than two letters, potential matches are displayed
- [x] The user can clear the search input
- [x] When search starts, popular suggestions are displayed
- [x] When search starts, recent search history is displayed
- [x] When search starts, an empty suggestion state can be displayed
- [x] When a search is confirmed or selected, the corresponding catalog is displayed
- [x] More catalog results can be loaded
- [x] Confirmed searches are recorded in search history

Rule: While the user types more than two letters, potential matches are displayed
```yaml
Scenario: Display matches by game
  Given the user is typing a search with more than two letters
  When the entered text matches products associated with one or more games
  Then one game row is displayed for each related game

Scenario: Display matches by product or card
  Given the user is typing a search with more than two letters
  When the entered text matches a product or card
  Then at most 10 product rows are displayed
  And each product row displays the product name and "in [game]"
  And the portion of each product name matching the entered text is bold

Scenario: Display a search-in-catalog row
  Given the user is typing a search with more than two letters
  When autocomplete suggestions are displayed or the entered text does not match any available item
  Then a "View search in catalog" row is displayed
```

Rule: The user can clear the search input
```yaml
Scenario: Clear a written search
  Given the user has entered a search term
  When they select the clear icon at the right of the search input
  Then the search input is cleared
```

Rule: When search starts, popular suggestions are displayed
```yaml
Scenario: Display popular searches
  Given the user opens the search engine
  When they have not yet entered any search term
  Then at most 2 popular searches are displayed

Scenario: No popular items are available
  Given no popular searches or products are available
  When the user opens the search engine
  Then no popular suggestions are displayed
```

Rule: When search starts, recent search history is displayed
```yaml
Scenario: Display recent history
  Given the user has recent searches
  When they open the search engine
  Then their search history is displayed

Scenario: User without search history
  Given the user has no recent searches
  When they open the search engine
  Then no search history is displayed
```

Rule: When search starts, an empty suggestion state can be displayed
```yaml
Scenario: Display an empty suggestion state
  Given the user has no recent searches
  And no popular searches or products are available
  When the user opens the search engine
  Then an empty suggestion state is displayed
```

Rule: When a search is confirmed or selected, the corresponding catalog is displayed
```yaml
Scenario Outline: Open a catalog from a search query
  Given <search source> is available
  When the user <search action>
  Then the catalog corresponding to the search query is displayed
  And at most 48 catalog products are displayed

Examples: |
  | search source | search action |
  | a game suggestion | selects the game suggestion |
  | a popular search suggestion | selects the popular search suggestion |
  | a recent search suggestion | selects the recent search suggestion or confirms the search via click or enter |

Scenario: Open catalog from a product suggestion
  Given suggestions related to products are displayed
  When the user selects a product suggestion
  Then the corresponding product details are displayed

Scenario: The search returns no products
  Given the user has entered a search term
  When they confirm a search with no available products
  Then an empty results state is displayed
```

Rule: More catalog results can be loaded
```yaml
Scenario: Load more catalog results
  Given the catalog search has more than 48 products
  When the catalog is displayed
  Then the user can load more catalog products
  When the user requests more catalog products
  Then the next catalog products are added to the displayed catalog

Scenario: All catalog results are displayed
  Given the catalog search has no more products available
  When the catalog is displayed
  Then no option to load more catalog products is displayed
```

Rule: Confirmed searches are recorded in search history
```yaml
Scenario: Record a confirmed search
  Given the user has entered a search term
  When they confirm the search via click or enter
  Then the search term is recorded as their most recent search
```
