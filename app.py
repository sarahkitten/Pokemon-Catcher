from flask import Flask, render_template, flash, request, redirect
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
from play_pokemon_catcher import *


# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


pokedict = make_pokedict()
pokedex = set()
p_type = None
catalog = None
to_go = None


class ReusableForm(Form):
    name = StringField('Catch a Pokemon:', validators=[validators.required()])

    @app.route("/", methods=['GET', 'POST'])
    def get_type():
        global pokedict
        global pokedex
        global p_type
        global catalog
        global to_go
        pokedict = make_pokedict()
        pokedex = set()
        p_type = None
        catalog = None
        to_go = None
        name = 'Something went wrong'

        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            name = request.form['name'].capitalize()
            print(name)
            if name.lower() in ["normal", "fire", "fighting", "water", "flying",
                               "grass", "poison", "electric", "ground", "psychic",
                               "rock", "ice", "bug", "dragon", "ghost", "dark",
                               "steel", "fairy"]:
                p_type = name
            else:
                flash("Whoops! Did you spell that right?")
        if p_type:
            catalog = make_catalog(pokedict, p_type)
            to_go = len(catalog)
            return redirect('/catch')
        return render_template('type.html', form=form)

    @app.route("/catch", methods=['GET', 'POST'])
    def catch():
        global to_go
        name = 'Something went wrong'

        form = ReusableForm(request.form)

        print(form.errors)
        if request.method == 'POST':
            name = request.form['name'].capitalize()
            print(name)

        if form.validate():
            # Save the comment here.
            if name in pokedex:  # already caught mon
                flash(f"Whoops! You already have {name}!")

            elif name not in catalog:  # wrong type
                if name in pokedict:
                    flash(f'Whoops! {name} is {pokedict[name]} type')

                else:  # misspelling
                    flash("Whoops! Did you spell that right?")

            else:  # caught mon
                catalog.remove(name)
                pokedex.add(name)
                to_go -= 1
                if to_go != 0:
                    flash(f"You caught {name}!")
                else:  # caught all mons
                    return redirect('/you-win')

        flash(f"{to_go} {p_type} types left!")

        return render_template('catch.html', form=form)

    @app.route("/give-up", methods=['GET', 'POST'])
    def give_up():
        global catalog
        for mon in catalog:
            flash(mon)
        return render_template('give-up.html')

    @app.route('/you-win', methods={'GET', 'POST'})
    def win():
        return render_template('you-win.html')




if __name__ == "__main__":
    app.run()