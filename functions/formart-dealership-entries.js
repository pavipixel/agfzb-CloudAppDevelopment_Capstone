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
  return {
    entries: params.docs.map((row) => { return {
      id: row.id,
      city: row.city,
      st: row.st,
      state: row.state,
      short_name: row.short_name,
      full_name: row.full_name,
      address: row.address,
      zip: row.zip,
      lat: row.lat, 
      long: row.long
    }})
  };
}