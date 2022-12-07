"""
Created on Wed Dec 06 2022

@author: Chin-Yeh Chen
"""
import os
import pandas as pd
import proj2proj_CY as p2p


def degdecimal2UTM50N(df):
    """
    lon&lat(degreeOfDecimal) converting to UTM50N by using segy2segy
    """
    lon = df["cdpx_ll"].values.tolist()
    lat = df["cdpy_ll"].values.tolist()

    return p2p.segy2segy(s_srs=4326, t_srs=32650, X=lon, Y=lat)


def main_coor_ll2utm(pathO, file, file_name, ext):
    """
    main
    """
    data = pathO + "\\input_ll\\" + file
    df = pd.read_csv(data, sep=",", header=0)
    df.set_axis(['cdp', 'cdpx_ll', 'cdpy_ll'], axis='columns', inplace=True)

    ## ll2UTM
    data_ll = degdecimal2UTM50N(df)

    df['cdpx'] = data_ll['cdpx']
    df['cdpy'] = data_ll['cdpy']

    # cdp fill zero
    cdp_zero = []
    for e in df['cdp']:
        if e != 'cdp':
            cdp_zero.append(str(e).zfill(7)) # 0000001
            # cdp_zero.append(format(e, '.7e')) # scientific notation
    df['cdp'] = cdp_zero

    # prepare final output
    output_folder_path = pathO + "\\output_utm\\"
    if not os.path.isdir(output_folder_path):
        os.makedirs(output_folder_path, mode=0o777)

    out_file_path = output_folder_path + file_name + "_utm." + ext
    d = {'cdp': df['cdp'], 'cdpx': df['cdpx'], 'cdpy': df['cdpy']}
    df_out = pd.DataFrame(data=d)
    df_out.to_csv(index=False, sep=' ', path_or_buf=out_file_path) #vital: for g2, sep has to be ''.

    # open output file automatically
    os.startfile(out_file_path)
    print('Done')


def csvtxt_checker(ext):
    """
    file extension checker
    """
    flag = False
    if ('txt' == ext):
        flag = True
    if ('csv' == ext):
        flag = True
    return  flag


def main():
    pathO = os.getcwd()
    input_folder = pathO + '\\input_ll\\'
    files = os.listdir(input_folder)
    for file in files:
        print('------------------------>')
        print(f'This is {file}:')
        s = file.split('.')
        file_name = s[0]
        ext = s[-1]
        if(len(s) < 1):
            print(f'Check file name')
            continue
        if (not csvtxt_checker(ext)):
            print(f'Check the file format please!')
            print("The .csv or .txt format are better choose.")
            continue
        main_coor_ll2utm(pathO, file, file_name, ext)


# -----------------------------------------------------------------------
# main start from here
main()