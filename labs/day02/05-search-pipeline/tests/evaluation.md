# Retrieval evaluation worksheet

The relevant IDs below describe intended relevance, not observed model rankings.
For each query record top-1 and top-3 IDs, scores, whether the relevant item
appeared, and differences between keyword and semantic modes. Model scores and
order can vary. Scores across the two methods are not directly comparable.

| Question | Relevant IDs | Top-1 / top-3 | Observations |
| --- | --- | --- | --- |
| How do I deploy an application to Kubernetes? | K8S-DEPLOY | | |
| My container keeps restarting, how can I investigate? | K8S-HEALTH | | |
| How do clients authenticate using a bearer token? | API-AUTH | | |
| Why do I get a 401 when my access token expires? | API-EXPIRED | | |
| How can I make a slow SQL query faster? | DB-INDEX | | |
| Why can my application not acquire a database connection? | DB-POOL | | |
| What should I inspect when a service goes down? | OPS-LOG | | |
| How should I retry temporary API failures? | OPS-RETRY | | |
| How do I configure a payment gateway? | None: no relevant article | | |

For the first eight questions, compute hit rate@3 as the number of questions
with at least one relevant ID in the top three divided by eight. Inspect the
out-of-scope question separately: nearest-neighbor search still returns results
even when nothing is relevant. Do not assume a universal score threshold.
