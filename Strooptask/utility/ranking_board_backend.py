# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 12:09:36 2024

@author: PC
"""
def msmain():
    #%%
    import os
    import glob
    import pickle
    import numpy as np
    import pandas as pd
    
    stroop_savepath = r'saved_data' + '\\'
    file_list = os.listdir(stroop_savepath)
    # 모든 폴더를 리스트업
    folders_list = []
    # 각 폴더의 block1 폴더 내의 *.pkl 파일을 찾음
    pkl_files_list = []
    folders_list_valid = []
    for folder in file_list:
        for block in ['block1']:
            block_path = os.path.join(stroop_savepath, folder, block)
            if os.path.exists(block_path):
                files = os.listdir(block_path)
                if len(files) == 49:
                    folders_list_valid.append(block_path)
                    
    #%%
    import sys
    sys.path.append(r'utility')
    import os
    import ranking_board_backend_학회종합용
    import stroop_score_calgen
    #%%
    
    import pandas as pd
    excel_path = 'features_output.xlsx'
    if not(os.path.exists(excel_path)):
        df = pd.DataFrame()  # 빈 데이터프레임
        df.to_excel(excel_path, index=False)
        print(f"{excel_path} 파일이 없어서 빈 파일을 새로 생성했습니다.")
        
    df = pd.read_excel(excel_path)
    features = []
    for index, row in df.iterrows():
        feature_dict = {
            'msid': row['msid'],  
            'date': row['date'],                      # 'msid' 열에서 값 추출
            'total_score': row['total_score'],                # 'score' 열에서 값 추출
            'netural_rt': row['netural_rt'],            # 'netural_rt' 열에서 값 추출
            'congruent_rt': row['congruent_rt'],        # 'congruent_rt' 열에서 값 추출
            'incongruent_rt': row['incongruent_rt'],    # 'incongruent_rt' 열에서 값 추출
            'netural_acc': row['netural_acc'],          # 'netural_acc' 열에서 값 추출
            'congruent_acc': row['congruent_acc'],      # 'congruent_acc' 열에서 값 추출
            'incongruent_acc': row['incongruent_acc']   # 'incongruent_acc' 열에서 값 추출
        }
        
        # features 리스트에 feature_dict 추가
        features.append(feature_dict)
    msid_list = [feature['msid'] for feature in features]
    
    for j in range(len(folders_list_valid)):
        second_subdir = os.path.basename(os.path.dirname(folders_list_valid[j]))
        underbar_ixs = [i for i, char in enumerate(second_subdir) if char == '_']
        msid = second_subdir[underbar_ixs[0]+1:]
        date = second_subdir[:underbar_ixs[0]]
        
        if not msid in msid_list:
            mssave_dict = ranking_board_backend_학회종합용.\
                msmain(pkl_path = folders_list_valid[j], tnum=49)
            
            data = [mssave_dict['block1']['neutral']['true_reatction_time'],
            mssave_dict['block1']['congruent']['true_reatction_time'],
            mssave_dict['block1']['incongruent']['true_reatction_time'], 
            mssave_dict['block1']['neutral']['acc'],
            mssave_dict['block1']['congruent']['acc'],
            mssave_dict['block1']['incongruent']['acc']]
            
            data = np.reshape(np.array(data), (6,1))
            # data[2] =  200
            score, z_scores = stroop_score_calgen.stroop_tscore(data)
    
            feature_dict = {
                'date': date,
                'msid': msid,
                'total_score': score[0],
                'netural_rt': data[0][0],
                'congruent_rt': data[1][0],
                'incongruent_rt': data[2][0],
                'netural_acc': data[3][0],
                'congruent_acc': data[4][0],
                'incongruent_acc': data[5][0],
            }
            features.append(feature_dict)
            
            print()
            print(feature_dict)
    
    df = pd.DataFrame(features)
    # output_filename = 'features_output.xlsx'
    df.to_excel(excel_path, index=False)

#%%




    
    
    
    