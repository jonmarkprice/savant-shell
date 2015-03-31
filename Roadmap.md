# Roadmap #

## Savant 0.9 ##
  * Savant Server Implementation
    * Develop a single threaded server to communicate with the front-end.
    * Ensure message passing is JSON/REST compliant.
  * Extensibility Support
    * Externalizing grammar rules to allow adding new rules without changing the lexer and the parser.
    * Make a handful of result renderers available to grammar extensions.
  * Java/Swing Front-end
    * Syntax auto-completion based on command.
    * Extended panel to view query results with different types of rendering.

## Savant 1.0 ##
  * Web Services Integration
    * Add rules to poll results from popular web services like Facebook, Google Calendar, Flickr etc.
    * Add rules to push/pipe user data to these web-services.
  * `[Optional]` [Beagle](http://beagle-project.org/Main_Page) integration
    * Using Beagle Python API to perform content based queries.
    * Extend scope of queries to everything that Beagle can index.

## Savant 2.0 ##
  * Advanced Extensibility
    * Implement the front-end on an RIA platform (e.g. Adobe AIR, Titanium, JavaFX).
    * Port existing result renderers to RIA supported scripting language.
    * Make parsing result format JSON/REST-compliant.
    * Allow custom result renderers to be added alongside grammar extensions.