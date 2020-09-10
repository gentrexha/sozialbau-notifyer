# OSM Transferlist Analyzer

## Getting started

Have a webdriver inside the `src` directory or in your `PATH`.

Also have a `.env` file inside the project folder that looks like this:
````
manager-name=
password=
fb-username=
fb-password=
driver=
````

Execute the commands

```
python ./src/get_data.py
python ./src/update_data.py
python ./src/message.py
```

, and you'll end up with the a `players.csv`

## TODO

- [ ] Include Nationality in data export