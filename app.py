import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'cook_book'
app.config["MONGO_URI"] = os.getenv('MONGO_URI', 'mongodb://localhost')

mongo = PyMongo(app)



@app.route('/')
def home_page():
    return render_template("home.html")

# RECIPE
# Gets recipes from mongo 
@app.route('/get_recipes')
def get_recipes():
    return render_template("recipes.html", 
                           recipes=mongo.db.recipes.find())


# Add recipe in database
@app.route('/add_recipe')
def add_recipe():
    return render_template('addrecipe.html',
                         categories=mongo.db.categories.find())


# Read full decription of single recipe
@app.route('/recipe/<recipe_id>')
def recipe_description(recipe_id):
    the_recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("recipe_description.html", recipe=the_recipe)



# Inserting recipes into database
@app.route('/insert_recipe', methods=['POST'])
def insert_recipe():
    recipes =  mongo.db.recipes
    recipes.insert_one(request.form.to_dict())
    return redirect(url_for('get_recipes'))


# Updating recipe in database
@app.route('/edit_recipe/<recipe_id>')
def edit_recipe(recipe_id):
    the_recipe =  mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    all_categories =  mongo.db.categories.find()
    return render_template('editrecipe.html', recipe=the_recipe,
                           categories=all_categories)


# Updating recipes after editing
@app.route('/update_recipe/<recipe_id>', methods=["POST"])
def update_recipe(recipe_id):
    recipes = mongo.db.recipes
    recipes.update( {'_id': ObjectId(recipe_id)},
    { 
        'category_name':request.form.get('category_name'),
        'recipe_name':request.form.get('recipe_name'),
        'recipe_description': request.form.get('recipe_description'),
        'recipe_ingredient':request.form.get('recipe_ingredient'),
        'recipe_direction':request.form.get('recipe_direction'),
        'post_date': request.form.get('post_date'),
    })
    return redirect(url_for('get_recipes'))


# deleting recipe
@app.route('/delete_recipe/<recipe_id>')
def delete_recipe(recipe_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipe_id)})
    return redirect(url_for('get_recipes'))



# CATEGORIES
# list all category in databases
@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


# Render template for adding new category
@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')  


# Insert new category into database
@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


# Upadting category in database
@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))


# Updating category after editing
@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
    mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))
    
    
# Render template for deleting category
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


# CUISINES
# list all cuisines in databases
@app.route('/get_cuisines')
def get_cuisines():
    return render_template('cuisines.html',
                           categories=mongo.db.cuisines.find())


# Render template for adding new category
@app.route('/add_cuisine')
def add_cuisine():
    return render_template('addcuisine.html')  


# Insert new category into database
@app.route('/insert_cuisine', methods=['POST'])
def insert_cuisine():
    cuisine_doc = {'cuisine_name': request.form.get('cuisine_name')}
    mongo.db.cuisines.insert_one(cuisine_doc)
    return redirect(url_for('get_cuisines'))


# Upadting category in database
@app.route('/edit_cuisine/<cuisine_id>')
def edit_cuisine(cuisine_id):
    return render_template('editcuisine.html',
    cuisine=mongo.db.cuisines.find_one({'_id': ObjectId(cuisine_id)}))


# Updating category after editing
@app.route('/update_cuisine/<cuisine_id>', methods=['POST'])
def update_cuisine(cuisine_id):
    mongo.db.cuisines.update(
        {'_id': ObjectId(cuisine_id)},
        {'cuisine_name': request.form.get('cuisine_name')})
    return redirect(url_for('get_cuisines'))
    
    
# Render template for deleting category
@app.route('/delete_cuisine/<cuisine_id>')
def delete_cuisine(cuisine_id):
    mongo.db.cuisines.remove({'_id': ObjectId(cuisine_id)})
    return redirect(url_for('get_cuisines'))



if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)