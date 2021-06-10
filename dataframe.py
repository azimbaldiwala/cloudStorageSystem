import pandas as pd


def dataframe(filename, file_size):
    sr_no = []
    for x in range(1, len(filename) + 1):
        sr_no.append(x)

    df = pd.DataFrame(
        {'Filename': filename, 'Filesize in KB': file_size},
        columns=['Filename', 'Filesize in KB'], index=sr_no)
    return df.to_html()
