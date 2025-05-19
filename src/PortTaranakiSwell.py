import easyocr
import requests
import cv2
import pandas as pd
import os
import random

def get_image():
    filepath = (['EnviewJSummary.jpg', 'EnviewJTriaxysWave.jpg'])
    img_url_base = 'https://www.porttaranaki.co.nz/sea-conditions-feeds/'
    for i in range(0, len(filepath)):
        img_url = img_url_base + filepath[i] + '?lt=1747596540'
        r = requests.get(img_url)
        additional = random.randint(100, 999)
        img_url = img_url_base + filepath[i] + '?lt=1747596540' + str(additional)
        r = requests.get(img_url)
        sc = r.status_code
        if r.status_code == 200:
            with open(filepath[i], 'wb') as f:
                f.write(r.content)
        else: print(f"status_code {sc} {filepath[i]}")
        
get_image()

def crop_image():
    reader = easyocr.Reader(['en'], gpu = False)
    img_triaxys = cv2.imread("EnviewJTriaxysWave.jpg")
    img_summary = cv2.imread("EnviewJSummary.jpg")
    #recorded_dt = datetime.now()
    
    file_name = 'df_swell_data.csv'
    if os.path.exists(file_name):
        df_swell_data = pd.read_csv(file_name)
    else:
        df_swell_data = pd.DataFrame(columns = ['measurement', 'value', 'measure_datetime'])
    
    # Get the date time first.
    cropped_triaxys_img_dt = img_triaxys[0:22, 832:1016] # bounding points for datetime
    cv2.imwrite('cropped_image_triaxys_dt.jpg', cropped_triaxys_img_dt)
    new_img_triaxys_dt = 'cropped_image_triaxys_dt.jpg'
    results_triaxys_dt = reader.readtext(new_img_triaxys_dt)
    df_text_triaxys_dt = pd.DataFrame(results_triaxys_dt, columns=['bbox', 'text', 'confidence'])
    swell_dt = df_text_triaxys_dt['text'].iloc[0]
    
    cropped_summary_img = img_summary[45:120, 110:295] # bounding points for triaxys buoy text
    cv2.imwrite('cropped_image_summary.jpg', cropped_summary_img)
    new_img_summary = "cropped_image_summary.jpg"
    results_summary = reader.readtext(new_img_summary)
    df_text_summary = pd.DataFrame(results_summary, columns=['bbox', 'text', 'confidence'])
    n_summary = len(df_text_summary) -1
    swell_direction = pd.DataFrame({"measurement": 'Swell Direction', "value": df_text_summary['text'].iloc[n_summary], "measure_datetime": swell_dt}, index=[0])
    #df_text_summary['dt'] = swell_dt
    
    cropped_triaxys_img = img_triaxys[27:225, 881:970] #bounding points for triaxys data
    cv2.imwrite('cropped_image_triaxys.jpg', cropped_triaxys_img)
    new_img_triaxys = "cropped_image_triaxys.jpg"
    results_triaxys = reader.readtext(new_img_triaxys)
    df_text_triaxys = pd.DataFrame(results_triaxys, columns=['bbox', 'text', 'confidence'])
    peak_period = pd.DataFrame({"measurement": 'Peak Period', "value": df_text_triaxys['text'].iloc[0], "measure_datetime": swell_dt}, index=[0])
    mean_period = pd.DataFrame({"measurement": 'Mean Period', "value": df_text_triaxys['text'].iloc[1], "measure_datetime": swell_dt}, index=[0])
    max_wave = pd.DataFrame({"measurement": 'Max Wave', "value": df_text_triaxys['text'].iloc[2], "measure_datetime": swell_dt}, index=[0])
    highest_10th = pd.DataFrame({"measurement": 'Highest 10th', "value": df_text_triaxys['text'].iloc[3], "measure_datetime": swell_dt}, index=[0])
    sig_height = pd.DataFrame({"measurement": 'Sig Height', "value": df_text_triaxys['text'].iloc[4], "measure_datetime": swell_dt}, index=[0])
    df_swell_data = pd.concat([df_swell_data, peak_period, mean_period, max_wave, highest_10th, sig_height, swell_direction], ignore_index=True)
    
    df_swell_data = df_swell_data.drop_duplicates() #need to remove recorded_dt to work
    df_swell_data.to_csv('df_swell_data.csv', index_label=False)    
    
    return(df_swell_data)

def swell_parameters():
    df_swell = crop_image()
    df_swell = df_swell.tail(6)
    s_peak_period = df_swell['value'].iloc[0]
    s_mean_period = df_swell['value'].iloc[1]
    s_max_height = df_swell['value'].iloc[2]
    s_highest_10th = df_swell['value'].iloc[3]
    s_sig_height = df_swell['value'].iloc[4]
    s_swell_dir = df_swell['value'].iloc[5]
    print(f"Peak Period {s_peak_period}")
    print(f"Mean Period {s_mean_period}")
    print(f"Max Height {s_max_height}")
    print(f"Highest 10th {s_highest_10th}")
    print(f"Sig Height {s_sig_height}")
    print(f"Swell Direction {s_swell_dir}")

swell_parameters()