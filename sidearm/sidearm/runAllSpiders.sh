rm guelph.json
scrapy crawl guelph -o guelph.json

rm sidearm_common.json
scrapy crawl sidearm_common -o sidearm_common.json

rm dalhousie_stfx.json
scrapy crawl dalhousie_stfx -o dalhousie_stfx.json

rm geegees.json
scrapy crawl geegees -o geegees.json