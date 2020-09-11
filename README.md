# OSM Transferlist Analyzer

## Getting started

Have a webdriver inside the `src` directory or in your `PATH`.

Also have a `.env` file inside the project folder that looks like this:
````
manager-name=
password=
driver=
bot_token=
bot_chatID=
````

After that just execute 

```bash
python src/get_data.py
python src/update_data.py
python src/message.py
pause
```

## TODO

- [ ] Include Nationality in data export