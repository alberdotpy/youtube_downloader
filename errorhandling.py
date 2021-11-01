def error_handling(e):
    if str(e) == "'NoneType' object has no attribute 'download'":
        print('The chosen resolution was not available for this video, please, try choosing 360p or 480p')
    else:
        print(e)