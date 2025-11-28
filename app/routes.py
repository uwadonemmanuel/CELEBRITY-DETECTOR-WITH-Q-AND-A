from flask import Blueprint,render_template,request

from app.utils.image_handler import process_image
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.qa_engine import QAEngine

import base64

main = Blueprint("main" , __name__)

celebrity_detector = CelebrityDetector()
qa_engine = QAEngine()

@main.route("/" , methods=["GET" ,"POST"])
def index():
    player_info = ""
    player_name = ""
    result_img_data = ""
    user_question = ""
    answer = ""


    if request.method == "POST":
        if "image" in request.files:
            image_file = request.files["image"]

            if image_file:
                img_bytes , face_box = process_image(image_file)

                player_info , player_name = celebrity_detector.identify(img_bytes)

                if face_box is not None:
                    result_img_data = base64.b64encode(img_bytes).decode()
                else:
                    player_info="No face detected Please try another image"
                    player_name = ""  # Clear player_name if no face detected

        elif "question" in request.form:
            user_question = request.form["question"]

            player_name = request.form.get("player_name", "")
            player_info = request.form.get("player_info", "")
            result_img_data = request.form.get("result_img_data", "")

            # Only ask the QA engine if we have a valid player name (not an error message)
            if player_name and not player_name.startswith("Error:") and player_name.strip() != "":
                answer = qa_engine.ask_about_celebrity(player_name,user_question)
            else:
                answer = "Error: Cannot answer questions. No valid celebrity was detected. Please upload an image first."

    # Determine if we have a valid celebrity (not an error message)
    has_valid_celebrity = (
        player_info and 
        not player_info.startswith("Error:") and 
        not player_info.startswith("Unknown") and
        "**Full Name**" in player_info
    )
    
    return render_template(
        "index.html",
        player_info=player_info,
        player_name=player_name,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer,
        has_valid_celebrity=has_valid_celebrity
    )
    




        



                

