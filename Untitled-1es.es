GET news/_search
{
    "query" : {
        "match" : {
            "text" : "손흥민"
        }
    }
}

GET news/_search
{
    "query": {
        "match": {
            "text": "손흥민"
        }
    }
}