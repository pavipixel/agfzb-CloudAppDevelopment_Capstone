/**
  *
  * main() will be run when you invoke this action
  *
  * @param Cloud Functions actions accept a single parameter, which must be a JSON object.
  *
  * @return The output of this action, which must be a JSON object.
  *
  */
 function main(params) {
    if(params.state){
        return { 
            "query": 
            {
                "selector": {
                    "st": params.state
                },
                "fields": ["id", "st", "state", "city", "short_name", "full_name", "address", "zip", "lat", "long"]
            }
        }
    }
    else
    {
        return { 
            "query": 
            {
                "selector": {},
                "fields": ["id", "st", "state", "city", "short_name", "full_name", "address", "zip", "lat", "long"]
            }
        }
    }
}
