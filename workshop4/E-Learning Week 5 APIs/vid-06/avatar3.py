from flask import (
    Flask, request, abort, 
    render_template, url_for, 
    jsonify, send_file
    )
from flasgger import Swagger

# aang, katara, sokka, toph, iroh, zuko
master_dict = {
    'aang':  "The last Airbender, Aang embraces his Avatar destiny, mastering four elements, defeating the Fire Nation, and restoring world balance.",
    'katara': "A skilled waterbender, Katara grows from an idealistic girl into a powerful warrior, healer, and advocate for justice and change.",
    'sokka': "A brilliant strategist, Sokka compensates for no bending with intelligence, humor, and bravery, becoming essential to Team Avatar’s success.",
    'zuko': "Exiled Fire Nation prince, Zuko seeks honor, struggles with identity, and ultimately joins Aang, helping to restore peace.",
    'iroh': "A wise, tea-loving general, Iroh mentors Zuko, emphasizing balance, kindness, and redemption despite his Fire Nation past.",
    'toph': "A blind earthbender, Toph invents metalbending, proving strength comes from independence, resilience, and defying expectations."
    }

image_dict = {
    'aang'  : 'aang.png',
    'katara': 'katara.png',
    'sokka' : 'sokka.png',
    'zuko'  : 'zuko.png',
    'iroh'  : 'iroh.png',
    'toph'  : 'toph.png'
    }

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/list/characters", methods=["GET"])
def get_all_characters():
    """
    Lists all characters on the server.
    ---
    responses:
      200:
        description: Lists all characters.
    """
    char_names = [x.title() for x in master_dict.keys()]
    return render_template('chars.html', char_names = char_names, 
                           list_type="characters")

@app.route("/list/images", methods=["GET"])
def get_all_images():
    """
    Lists all images on the server.
    ---
    responses:
      200:
        description: Lists all image filenames.
    """
    image_names = [x for x in image_dict.values()]
    return render_template('chars.html', char_names = image_names,
                           list_type="images")

@app.route("/character/<string:name>", methods=["GET"])
def display_character(name):
    """
    Displays a single character
    ---
    parameters:
      - name: name 
        in: path
        type: string
        required: true
        description: name of character to display.
    responses:
      200:
        description: Returns a HTML page with image and description
    """
    name = name.lower()
    dir_path = "images"
    if name in image_dict: 
        fname = image_dict[name]
        fpath = '/'.join([dir_path, fname])

        im_url = url_for('static', filename=fpath)
        if name in master_dict:
            descr1 = master_dict[name]
        else:
            descr1 = ""
        
        return render_template('single_char.html', 
                               name = name.title(),
                               image_url = im_url,
                               char_description=descr1)
    else:
        abort(400, "No such character present.")

@app.route("/download/<string:name>", methods=["GET"])
def download_image(name): 
    """
    Downloads a single image.
    ---
    parameters:
      - name: name 
        in: path
        type: string
        required: true
        description: character's image to display
    responses:
      200:
        description: Returns an image of the character 
    """
    name = name.lower()
    if name not in image_dict: 
        abort(400, "Image does not exist")
    else:
        path_to_image = 'static/images/' + image_dict[name]
        # url_to_image = url_for('static', filename=path_to_image) 
        return send_file(path_to_image)

@app.route("/modify/<string:name>", methods=["PUT", "POST"])
def modify_character(name):
    name = name.lower()
    # check username password
    u_name = request.authorization.parameters['username']
    pw = request.authorization.parameters['password']
    if (u_name != 'root') or (pw != 'pw'):
        abort(400, "username/password incorrect.")

    output_dict = {}

    if request.method == "PUT":
        if name not in master_dict:
            abort(400, "Name does not exist")
        new_desc = request.get_data(as_text=True)
        master_dict[name] = new_desc
        return jsonify(f"Description for {name} modified.")
    else:
        new_desc = request.get_data(as_text=True)
        master_dict[name] = new_desc
        return jsonify(f"Description for {name} added.")

@app.route("/delete", methods=["DELETE"])
def delete_character():
    name = request.args['name'].lower()
    u_name = request.authorization.parameters['username']
    pw = request.authorization.parameters['password']

    output_dict = {}

    if (u_name == "root") & (pw == "pw"):
        if name in image_dict:
            image_dict.pop(name)
            output_dict['image'] = 'removed'
        else:
            output_dict['image'] = 'not found'
        if name in master_dict:
            master_dict.pop(name)
            output_dict['description'] = 'removed'
        else:
            output_dict['description'] = 'not found'
    else:
        abort(400, "username/password incorrect.")

    return jsonify(output_dict)

@app.route("/gallery", methods=["GET"])
def make_gallery(): 
    img1 = request.args.get("img1")
    print(img1)
    img2 = request.args.get("img2")
    print(img2)
    img3 = request.args.get("img3")
    print(img3)

    name_list = [img.lower() for img in [img1, img2, img3] if img]
    img_paths = ['images/' + image_dict[x] for x in name_list if x in image_dict]
    urls = [url_for('static', filename=fname) for fname in img_paths]
    print(urls)
    return render_template('gallery.html', img_urls = urls)
