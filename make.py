import json
from jinja2 import Template


with open('data.json') as fin:
    data = json.load(fin)

raw = Template("""<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
	<link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
	<link rel="stylesheet" type="text/css" href="style.css">
	<!-- Font from here: http://www.fontspace.com/jackster-productions/pokemon-gb -->
	<script>
	  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
	  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
	  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
	  })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');
	  ga('create', 'UA-100873215-1', 'auto');
	  ga('send', 'pageview');
	</script>
	<title>{{ page_title }}</title>
</head>
<body>
<div class="container-fluid">
    <div class="jumbotron">
        <h1 class="display-1">{{ top_heading }}</h1>
        <p class="display-5">{{ subtitle }}</p>
    </div>
    <div class="container">
		<img class="mx-auto d-block mb-4" src="img/gif/{{ map }}" alt="Pokémon style map of the Bay Area">
		<div class="row">
		{% for n in data['header']['notes'] %}
		{% if loop.index == 4 %}
        <div class="col-12 mb-4">
            <div class="card">
                <div class="card-body">{{ n['text'] }}</div>
            </div>
        </div>
        {% else %}
        <div class="col-xs-12 col-md-6 col-lg-4 mb-4">
            <div class="card">
                <div class="card-body">{{ n['text'] }}</div>
            </div>
        </div>
        {% endif %}
		{% endfor %}
		</div>
	</div>
	{% for s in data['body'] %}
    <section>
        <div class="jumbotron day-{{ loop.index }}">
          <h2 class="display-5">{{ s['hero']['title'] }}</h2>
        </div>
        <section class="container">
            <div class="row">
            {% for n in s['notes'] %}
                <div class="col-xs-12 col-md-6 col-lg-4 mb-4">
                    <div class="card">
                        {% if n.get('image') %}
                        <img class="card-img-top h-100" src="img/25_percent/{{ n['image'] }}" alt="two gyms">
                        {% endif %}
                        <div class="card-body">{{ n['text'] }}</div>
                    </div>
                </div>
            {% endfor %}
            {% if s.get('tables') %}
            {% for t in s['tables'].keys() %}
                <div class="col mb-4">
                    <div class="card">
                        <h3 class="card-title mx-auto d-block m-4">{{ s['tables'][t]['title'] }}</h3>
                        <div class="table-responsive-sm">
                            <table class="table table-bordered">
                                <thead>
                                    <tr>
                                        {% for h in s['tables'][t]['header'] %}
                                        <th scope="col">{{ h }}</th>
                                        {% endfor %}
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for row in s['tables'][t]['content'] %}
                                    <tr>
                                        {% for k in row.keys() %}
                                            {% if k == 'image' %}
                                                <td>
                                                    {% for img in row['image'] %}
                                                        <img src="img/pkm_sprites/{{ img }}">
                                                    {% endfor %}
                                                </td>
                                            {% else %}
                                                <td>{{ row[k] }}</td>        
                                            {% endif %}
                                        {% endfor %}
                                    </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            {% endfor %}
            {% endif %}
            </div>
        </section>
    </section>
	{% endfor %}
	</div>
</body>
</html>""")

html = raw.render(page_title='pokéblog',
                  top_heading=data['header']['title'],
                  subtitle=f"{data['header']['time']} - {data['header']['subtitle']}",
                  map=data['header']['map'],
                  data=data
                  )


css = """@font-face {
	font-family: "Pokemon";
	src: url("font/pokemon_gb.ttf");
}

body {
	font-family: Pokemon, Verdana, Tahoma, monospace;
}

.card {  /* override Bootstrap card border for more original GB Pkmn style */
	border: 6px double black;
}

table img { width: 60px; }

ul {
	list-style-image: url("img/pokeball-bullet-point.png");
}

.jumbotron {  /* general code to allow for full-width background images with text on top (hero) */
	background-position: center;
	background-repeat: no-repeat;
	background-size: cover;
	text-align: center;
	color: white;
}

/* individual section background images below */"""

for i, s in enumerate(data['body'], start=1):
    hero_css = '\n.day-%s {background-image: url("img/heros/%s");}\n' % (i, s['hero']['background'])
    css += hero_css

with open('style.css', 'w') as style:
    style.write(css)

with open('indexxx.html', 'w') as index:
    index.write(html)