
# TV Show Catalog

This database keeps track of TV shows, the people who work on them, their genres, and ratings.

```mermaid
erDiagram
    SHOWS ||--o{ SHOW_GENRES : has
    GENRES ||--o{ SHOW_GENRES : categorizes
    SHOWS ||--o{ SHOW_PEOPLE : features
    PEOPLE ||--o{ SHOW_PEOPLE : works_on
    SHOWS ||--o| RATINGS : receives

    SHOWS {
        int show_id PK
        string title
        int release_year
        string show_type
        int episode_count
    }

    PEOPLE {
        int person_id PK
        string name
        int birth_year
    }

    GENRES {
        int genre_id PK
        string genre_name
    }

    SHOW_GENRES {
        int show_id PK,FK
        int genre_id PK,FK
    }

    SHOW_PEOPLE {
        int show_id PK,FK
        int person_id PK,FK
        string role PK
    }

    RATINGS {
        int show_id PK,FK
        float average_rating
        int vote_count
    }
```

## Assumptions

- Each show has its own ID, even if two shows have the same name.
- A person can work on multiple shows.
- People can be actors, writers, or both.
- A show can have more than one genre.
- Some shows might not have ratings yet.
- We might not know everyone's birth year.
- Some shows might not have an episode count available.
- Ratings show the overall score and number of votes, not every individual review.
