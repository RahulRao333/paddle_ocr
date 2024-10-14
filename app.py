import os
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from multiprocessing import Pool,Manager,freeze_support
import pytesseract
from pdf2image import convert_from_path
from pytesseract import image_to_string
import re
import pandas as pd
import shutil
from PIL import Image
import cv2
from datetime import datetime
from PyPDF2 import PdfWriter, PdfReader
import os
from paddleocr import PaddleOCR,draw_ocr


pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\Tesseract-OCR\tesseract.exe'

ocr = PaddleOCR(use_angle_cls=True, lang='en')

#img_path =r'D:\paddle_ocr\temp_images\page.png'


def count_files(directory):
    if os.path.exists(directory):
        return len(os.listdir(directory))
    else:
        return 0

def extract_data(image_path):
    pattern_type1 = r'[A-Z]{3}\d{7}'
    pattern_type2 = r'[A-Z]{2}/\d{2}/\d{3}/\d+'

    voter_data = []
    Name = []
    RelationName = []
    HouseNumber = []
    Age = []
    Gender = []
    pattern_name = r'Name :(.*)'
    pattern_name_2 = r'Name(.*)'
    pattern_fathername = r'Fathers Name:(.*)'
    pattern_husband = r'Husbands Name:(.*)'
    pattern_Others = r'Others:(.*)'
    pattern_Mother = r'Mothers Name:(.*)'
    pattern_house_number = r'House Number :(.*)'
    pattern_house_number_2 = r'House Number (.*)'
    pattern_house_number_3=r'House Number:(.*)'
    pattern_house_number_4 = r'House Number(.*)'

    pattern_age = r'Age : (.{3})'
    pattern_age_2 = r'Age (.{3})'
    pattern_age_3 = r'Age:(.{3})'
    pattern_age_4 = r'Age(.{3})'
    pattern_gender = r'Gender :(.*)'
    pattern_gender_2 = r'Gender (.*)'
    pattern_gender_3 = r'Gender:(.*)'
    pattern_gender_combined =r'Gender(.*)'

    result = ocr.ocr(image_path, cls=True)


    # Parse the OCR result and extract relevant information
    for line in result[0]:

        text = line[1][0]
        text = str(text)



        serial_numbers_type1 = re.findall(pattern_type1, text)
        if serial_numbers_type1:
            voter_data.append(serial_numbers_type1)
        # name_match = re.search(pattern_name, text)
        # if name_match:
        #     fam1=name_match.group(1).strip()
        #     Name.append(fam1)
        # else:
        #     name_match2 = re.search(pattern_name_2, text)
        #     if name_match2:
        #
        #             fam2 = name_match2.group(1).strip().split(',')
        #             Name.append(fam2)
                        # elif len(fam2)>=1:
                        #     RelationName.append(fam2[1])

        # fathername_match = re.search(pattern_fathername, text)
        # husband_match = re.search(pattern_husband, text)
        #
        # others_match = re.search(pattern_Others, text)
        # mother_match = re.search(pattern_Mother, text)
        # if fathername_match:
        #     RelationName.append(fathername_match.group(1).strip())
        # elif husband_match:
        #     RelationName.append(husband_match.group(1).strip())
        # elif others_match:
        #     RelationName.append(others_match.group(1).strip())
        # elif mother_match:
        #     RelationName.append(mother_match.group(1).strip())

        house_number_match = re.search(pattern_house_number, text)
        if house_number_match:
            HouseNumber.append(str(house_number_match.group(1).strip()))
        else:
            house_number_match = re.search(pattern_house_number_2, text)
            if house_number_match:
                HouseNumber.append(str(house_number_match.group(1).strip()))
            else:
                house_number_match3 = re.search(pattern_house_number_3, text)
                if house_number_match3:
                    HouseNumber.append(str(house_number_match3.group(1).strip()))
                else:
                    house_number_match4 = re.search(pattern_house_number_4, text)
                    if  house_number_match4:
                        HouseNumber.append(str(house_number_match4.group(1).strip()))


        #
        # age_match = re.findall(pattern_age, text)
        #
        # if age_match:
        #
        #     Age.append(age_match)
        # else:
        #     age_match = re.findall(pattern_age_2, text)
        #     if age_match:
        #         Age.append(age_match)
        #     else:
        #         age_match2 = re.findall(pattern_age_3, text)
        #         if age_match2:
        #             Age.append(age_match2)
        #         else:
        #             age_match3=re.findall(pattern_age_4,text)
        #             if age_match3:
        #                 Age.append(age_match3)
        #
        #
        #
        # gender_match = re.search(pattern_gender, text)
        # if gender_match:
        #     Gender.append(gender_match.group(1).strip())
        # else:
        #     gender_match2 = re.search(pattern_gender_2, text)
        #     if gender_match2:
        #         Gender.append(gender_match2.group(1).strip())
        #     else:
        #         gender_match3 = re.search(pattern_gender_3, text)
        #         if gender_match3:
        #             Gender.append(gender_match3.group(1).strip())
        #         else:
        #             gender_match4 = re.search(pattern_gender_combined, text)
        #             if gender_match4:
        #                 Gender.append(gender_match4.group(1).strip())
        #






    data = {
        "Serial Number": voter_data,
        "House Number": HouseNumber,
    }

    # # Append the extracted data for the current image to the list
    # extracted_data.append(data)
    return data

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'data'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
def parsing(pdf_path):
    images = convert_from_path(pdf_path)
    for i, image in enumerate(images):
        output_filename = f'pdf/output_image_{i}.png'
        image.save(output_filename, 'png')






def count_files(directory):
    files = os.listdir(directory)
    num_files = len(files)
    return num_files


def pooling_stations(args):
    try:
        imgpath,imgpath2 = args
        d3 = []


        counter = 0



        pattern_assembly_station = r'AssemblyConstituencyNoandName:(.*)'
        pattern_part = r'PartNo.:(.*)'
        section_part = r'SectionNoandName(.*)'
        #section_part2=r'SectionNoandName3(.*)'
        section_part2=r'1-ListofAdditions2(.*)'
        text = pytesseract.image_to_string(imgpath, lang='eng')
        textdata = " ".join(text)
        textdata = textdata.replace(" ", "")


        # match = re.search(pattern_assembly_station, textdata)
        # data2 = match.group(1).strip()
        #
        # match2 = re.search(pattern_part, data2)
        # if match2 == None:
        #     assembly = data2
        #     match3 = re.search(pattern_part, textdata)
        #     if match3 == None:
        #         missing = "New"
        #         Part_No = missing
        #     else:
        #         Part_No = match3.group(1).strip()
        #
        # else:
        #
        #     number = match2.group(1).strip()
        #     # print(number)
        #     Part_No = number
        #     data2 = data2.replace("PartNo.:" + number, "")
        #     assembly = data2

        match4 = re.search(section_part, textdata)
        matchnew=re.search(section_part2,textdata)
        if match4 == None and matchnew ==None:
            missing = "New"
            section = missing

        elif match4:
                section = match4.group(1).strip()

        else:
            section = matchnew.group(1).strip()


        new_dir="pdf"
        count = count_files(new_dir)
        count = int(count)
        directory =imgpath2
        count = count_files(directory)
        count = int(count)
        for k in range(count, 0, -1):





                d3.append(section)
        return d3



    except Exception as e:
        print(e)








def process_image_english(img_path):
    try:
        image = cv2.imread(img_path)
        if image is not None:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)
            edges = cv2.Canny(blurred, 50, 150)

            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            os.makedirs("images",exist_ok=True)
            output_dir = f'images/unorder_{os.path.basename(img_path)}'
            output_dir = output_dir.replace(".png", "")
            os.makedirs(output_dir, exist_ok=True)

            min_table_area = 1000
            j = 0
            for contour in contours:
                if cv2.contourArea(contour) > min_table_area:
                    x, y, w, h = cv2.boundingRect(contour)
                    cropped_table = image[y:y + h, x:x + w]
                    output_path = os.path.join(output_dir, f'cropped_table_{j}.png')

                    j += 1
                    cv2.imwrite(output_path, cropped_table)
                    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

            # directory = "D:/automation/paddle_ocr_testing//pdf"
            # items = os.listdir(directory)
            #
            # for k in range(len(items)):
            #     directory2 = f"D:/automation/paddle_ocr_testing/images/unorder_output_image_{k}"
            #     os.makedirs(directory2, exist_ok=True)
            #     for r in range(len(os.listdir(directory2))):
            #         image_path = os.path.join(directory2, f'cropped_table_{r}.png')
            #         image = cv2.imread(image_path)
            #
            #         # Specify the coordinates and dimensions of the ROI
            #         x, y, width, height = 300, 10, 520, 28# Example coordinates and dimensions for voter number
            #
            #
            #         # Crop the ROI using array slicing
            #
            #         cropped_image = image[y:y + height, x:x + width]
            #
            #         directory3 = f"D:/automation/paddle_ocr_testing/voter_number/unorder_output_image_number{k}"
            #
            #
            #         os.makedirs(directory3, exist_ok=True)
            #
            #
            #         output_path2 = os.path.join(directory3, f'cropped_table_{r}.png')
            #
            #
            #         # Save the cropped image
            #         cv2.imwrite(output_path2, cropped_image)

    except Exception as e:
        print(e)

@app.route('/')
def upload_form():
    #print("i am here")


    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    print("I am here ")
    if 'files[]' not in request.files:
        return jsonify({"error": "No files part"}), 400

    language = request.form.get('language')
    print(f'Selected language: {language}')

    files = request.files.getlist('files[]')

    file_paths = []

    if language=="english":
        filenumber=0
        start=datetime.now()
        dir = "data"
        os.makedirs(dir,exist_ok=True)
        print("i am here")

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                file_paths.append(file_path)
        data_frames3 = []
        data_frames2=[]
        data_frame_voter = []

        directory_d = 'data'
        combined_df = pd.DataFrame()

        total_pdfs = []
        for filename in os.listdir(directory_d):
            filename = "data/" + filename
            total_pdfs.append(filename)

        for pdf in total_pdfs:
            filenumber=filenumber+1
            pdf_path = pdf
            images = convert_from_path(pdf_path, first_page=1, last_page=3)

            # Initialize an empty string to store extracted text
            extracted_text = ''
            count = 0
            # Loop through each page/image
            section_part = r'Section No and Name(.*)'
            addition_part = r'List of Additions 1'
            addition_part2=r'List of Additions 2'
            for img in images:
                # Extract text from image using Pytesseract
                text = pytesseract.image_to_string(img, lang='eng')  # You can specify the language
                extracted_text += text

            match4 = re.search(section_part, extracted_text)

            # Print or save the extracted text

            output_pdf_path = pdf_path
            # when it is 3 page to delete match4 will return empty
            if match4:

                extracted_text3 = ''
                extracted_text2=''

                with open(pdf_path, 'rb') as infile:
                    reader = PdfReader(infile)
                    writer = PdfWriter()
                    lastpage = len(reader.pages)
                    firstpage = lastpage - 2     #total last 3 pages will be checked

                    images = convert_from_path(pdf_path, first_page=firstpage, last_page=lastpage)
                    for img in images:
                        text = pytesseract.image_to_string(img, lang='eng')  # You can specify the language
                        extracted_text3 =extracted_text3+ text

                    match5 = re.search(section_part, extracted_text3)
                    match6 = re.search(addition_part, extracted_text3)
                    match7 = re.search(addition_part2,extracted_text3)
                    if match5 or match6 or match7:
                        #where we have to delete two or one page
                        lastpage=len(reader.pages)
                        firstpage-lastpage-1
                        images = convert_from_path(pdf_path, first_page=firstpage, last_page=lastpage)
                        for img in images:
                            text = pytesseract.image_to_string(img, lang='eng')  # You can specify the language
                            extracted_text2 = extracted_text2 + text
                        match5 = re.search(section_part, extracted_text2)
                        match6 = re.search(addition_part, extracted_text2)
                        match7 = re.search(addition_part2, extracted_text2)

                        if match5 or match6 or match7:

                            for page_num in range(2,lastpage-2):
                                writer.add_page(reader.pages[page_num])
                            with open(output_pdf_path, 'wb') as outfile:
                                writer.write(outfile)
                        else:
                            for page_num in range(2, lastpage-1):
                                writer.add_page(reader.pages[page_num])
                            with open(output_pdf_path, 'wb') as outfile:
                                    writer.write(outfile)
                    else:
                        #delete last 3 pages

                        for page_num in range(2, lastpage - 3):
                            writer.add_page(reader.pages[page_num])

                        with open(output_pdf_path, 'wb') as outfile:
                            writer.write(outfile)

            # If match4 is not found, inform the user
            elif not match4:

                extracted_text3 = ''
                extracted_text2=''
                with open(pdf_path, 'rb') as infile:
                    reader = PdfReader(infile)
                    writer = PdfWriter()
                    lastpage = len(reader.pages)
                    firstpage = lastpage - 2
                    images = convert_from_path(pdf_path, first_page=firstpage, last_page=lastpage)
                    for img in images:
                        text = pytesseract.image_to_string(img, lang='eng')  # You can specify the language
                        extracted_text3=extracted_text3+text
                    match5 = re.search(section_part, extracted_text3)
                    match6 = re.search(addition_part, extracted_text3)
                    match7 = re.search(addition_part2, extracted_text3)
                    if match5 or match6 or match7:
                        lastpage=len(reader.pages)
                        firstpage=lastpage-1   #check last 3 pages
                        images = convert_from_path(pdf_path, first_page=firstpage, last_page=lastpage)
                        for img in images:
                            text = pytesseract.image_to_string(img, lang='eng')  # You can specify the language
                            extracted_text2 = extracted_text2 + text
                        match5 = re.search(section_part, extracted_text2)
                        match6 = re.search(addition_part, extracted_text2)
                        match7 = re.search(addition_part2, extracted_text2)

                        if match5 or match6 or match7:
                            for page_num in range(3, lastpage-1):
                                writer.add_page(reader.pages[page_num])

                            with open(output_pdf_path, 'wb') as outfile:
                                writer.write(outfile)
                        else:

                            for page_num in range(3, lastpage - 2):
                                writer.add_page(reader.pages[page_num])

                            with open(output_pdf_path, 'wb') as outfile:
                                writer.write(outfile)
                    else:


                        #will delete last 3 pages

                        for page_num in range(3, lastpage - 3):
                            writer.add_page(reader.pages[page_num])

                        with open(output_pdf_path, 'wb') as outfile:
                            writer.write(outfile)


            counter = 0
            pdf_path = pdf
            directory = "pdf"
            if os.path.exists(directory):
                # Remove the existing directory and its contents
                shutil.rmtree(directory)
            os.makedirs('pdf', exist_ok=True)

            parsing(pdf_path)
            # directory = "pdf"
            count = count_files(directory)
            count = int(count)

            # Create a Pool of worker processes


            # Process images in parallel

            try:
                pool = Pool()
                image_paths = [f"pdf/output_image_{i}.png" for i in range(0, count)]
                pool.map(process_image_english, image_paths)
                pool.close()
            except Exception as e:
                print(f"An error occurred during multiprocessing: {e}. Continuing with the rest of the images.")
            def count_file(directory):
                if os.path.exists(directory):
                    return len(os.listdir(directory))
                else:
                    return 0

            try:
                pool10 = Pool()

                image_path = [f"images/unorder_output_image_{j}/cropped_table_{i}.png"
                              for j in range(0, count)
                              if count_file(f'images/unorder_output_image_{j}') > 0
                              for i in range(count_files(f'images/unorder_output_image_{j}') - 1, -1, -1)]

                house = pool10.map(extract_data, image_path)
                house = pd.DataFrame(house)
                #house['Serial Number']=house['Serial Number'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace(',', '', regex=False)

                #house['House Number'] = house['House Number'].str.replace('[', '', regex=False).str.replace(']', '', regex=False).str.replace(',', '', regex=False)

                house.to_excel(f'epic/epic_{filenumber}.xlsx',index=False)
                #data_frames2.append(house)


                pool10.close()
            except Exception as e:
                print(e)

            try:
                    pool2 = Pool()

                    imgpath = [f"pdf/output_image_{i}.png" for i in range(count)]

                    imgpath2 = [f"images/unorder_output_image_{i}" for i in range(count)]



                    args_list = list(zip(imgpath, imgpath2))

                    results = pool2.map(pooling_stations, args_list)

                    # df = pd.DataFrame(data)
                    # df=df.transpose()
                    # print(df)

                    pooling_station = []

                    for result in results:
                        pooling_station.extend(result)
                    df_combined = pd.DataFrame({'section': pooling_station})


                    # df_column = df1.transpose()
                    #data_frames3.append(df_combined)

                    # Create a DataFrame from the collected data

                    df_combined.to_excel(f'station/combined_station{filenumber}.xlsx', index=False)

                    pool2.close()
                    pool2.join()
            except Exception as e:
                print(e)



                #     print("Total time spent:", counter+1)
            #final_df = pd.concat(data_frames2, ignore_index=True)
            #final_df.to_excel('newocr_voter_eng.xlsx', index=False)
            #final_df2 = pd.concat(data_frames3, ignore_index=True)
            #final_df2.to_excel('combined_polling_station.xlsx', index=False)
            shutil.rmtree('images')


            dir2 = "pdf"
            shutil.rmtree(dir2)
            end=datetime.now()
            print("total time",end-start)
    shutil.rmtree('data')
    os.makedirs('data', exist_ok=True)
    return jsonify({"message": "Files successfully uploaded with ocr", "file_paths": file_paths})




if __name__ == "__main__":
    app.run(debug=True,port=5003)














