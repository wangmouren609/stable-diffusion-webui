import requests


def is_health():
    # https://ai.auto-pai.cn/sdapi/v1/memory
    memory = requests.get('http://localhost:7860/sdapi/v1/memory').json()
    json = memory
    print(f'curent memory info is : {json}')

    cuda = json['cuda']
    if cuda['events']['oom'] > 0 :
        # service is already oom 
        print('service is already oom ')
        progress = requests.get('http://localhost:7860/sdapi/v1/progress').json()
        is_idel = progress['state']['job_count'] ==0
        if is_idel and cuda['system']['free'] < 1572864000:
            print('service is is_idel but free cuda memory is to low ,service is not health')
            return False
    
    return True


if __name__ == '__main__':

    if not is_health():
        raise Exception('service is not health')