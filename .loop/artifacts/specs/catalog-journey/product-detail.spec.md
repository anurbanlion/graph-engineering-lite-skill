Feature: Product Detail
The user can view a catalog product and navigate to its related catalog and seller destinations.

## Rules

- [ ] A product detail displays its canonical product information
- [ ] A product detail displays its available seller listings
- [ ] The user can order available seller listings
- [ ] The user can navigate from a product detail to related destinations
- [ ] The user can discover other prints of a card
- [ ] The user can start selling a card from its product detail

Rule: A product detail displays its canonical product information
```yaml
Scenario: Display an active product detail
  Given an active product exists for the requested product identifier
  When the user opens the product detail
  Then the product image, title, game, and expansion are displayed
  And the product details are displayed
  And the card information is displayed when it is available
  And card legality information is displayed when it is available

Scenario: Display a product without an associated expansion
  Given an active product has no associated expansion
  When the user opens the product detail
  Then the product information is displayed
  And no expansion navigation is displayed

Scenario: Requested product does not exist or is inactive
  Given no active product exists for the requested product identifier
  When the user opens the product detail
  Then a not found state is displayed
```

Rule: A product detail displays its available seller listings
```yaml
Scenario: Display the recommended available listing
  Given a product has a recommended available seller listing
  When the user opens the product detail
  Then the recommended listing displays its seller, condition, price, and delivery information

Scenario: Display multiple available seller listings
  Given a product has multiple available seller listings
  When the user opens the product detail
  Then each available seller listing displays its seller, condition, price, and delivery information

Scenario: Product without available seller listings
  Given a product has no available seller listings
  When the user opens the product detail
  Then the product information is displayed
  And no available seller listing is displayed
```

Rule: The user can order available seller listings
```yaml
Scenario: Display the default seller listing order
  Given a product has multiple available seller listings
  When the user opens the product detail
  Then the seller listings are ordered from lowest to highest price

Scenario: Order seller listings by the selected criterion
  Given a product has multiple available seller listings
  When the user selects a listing order criterion
  Then the seller listings are displayed in the selected order
```

Rule: The user can navigate from a product detail to related destinations
```yaml
Scenario: Navigate to the product game catalog
  Given the product detail displays the product game
  When the user selects the game navigation
  Then the catalog filtered by that game is displayed

Scenario: Navigate to the product expansion catalog
  Given the product detail displays an associated expansion
  When the user selects the expansion navigation
  Then the catalog filtered by that expansion is displayed

Scenario: Navigate to a seller profile
  Given an available seller listing displays its seller
  When the user selects the seller navigation
  Then the seller public profile is displayed
```

Rule: The user can discover other prints of a card
```yaml
Scenario: Navigate to other prints of a card
  Given the card product detail displays other prints navigation
  When the user selects other prints
  Then the catalog matching the card prints is displayed
```

Rule: The user can start selling a card from its product detail
```yaml
Scenario: Start selling the displayed card
  Given the card product detail displays sell this card navigation
  When the user selects sell this card
  Then the selling flow for that card is displayed
```

## Out of scope

- Selecting a purchase quantity
- Adding a product listing to the cart
- Buying a product listing now
