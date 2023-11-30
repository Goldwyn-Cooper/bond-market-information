import os, requests, polars as pl

# 이벤트 처리 함수: AWS Lambda와 같은 서버리스 환경에서 사용될 수 있습니다.
def handler(event=None, context=None):
    # 환경 변수에서 API URL을 가져옵니다.
    URL = os.getenv('API_URL')
    # 데이터를 가져오고 처리하는 함수를 호출합니다.
    result = fetch_and_process_data(URL)
    return {
        'result': result
    }

# 주어진 URL에서 데이터를 가져오고 처리하는 함수입니다.
def fetch_and_process_data(url: str) -> dict:
    # 주어진 URL에서 데이터를 요청합니다.
    response = requests.get(url)
    # JSON 형태의 응답에서 데이터를 추출합니다.
    data = response.json().get('body').get('반복데이타0')
    
    # 데이터를 Polars DataFrame으로 변환하고 행과 열을 전치합니다.
    df = pl.DataFrame(data).transpose()\
            .select(pl.all().str.strip_chars())
    # DataFrame의 열 이름을 설정합니다.
    df.columns = [
        '종목명', '매도수익률', '잔존일', '거래대금', '표면금리', 
        '신용도', '종목코드', '현재가', '상품구분', '이자방법', 
        '잔존만기연수', '잔존만기월수', '잔존만기일수', '매수수익률', 
        '표면금리2', 'x1', 'x2', '상환일', '거래량', '등락률', '전일종가'
    ]
    
    # 특정 열의 데이터 타입을 변환합니다.
    df = df.cast({
        '매도수익률': pl.Float64,
        '잔존일': pl.Int64,
        '거래대금': pl.Int64,
        '표면금리': pl.Float64,
        '현재가': pl.Float64,
        '잔존만기연수': pl.Int64,
        '잔존만기월수': pl.Int64,
        '잔존만기일수': pl.Int64,
        '매수수익률': pl.Float64,
        '표면금리': pl.Float64,
        '거래량': pl.Int64,
        '등락률': pl.Float64,
        '전일종가': pl.Float64,
    })
    
    # 사용하지 않는 열을 제거합니다.
    df = df.select(pl.exclude(['표면금리2', 'x1', 'x2']))
    # DataFrame을 사전 형태로 변환하여 반환합니다.
    return df.to_dicts()

# 메인 함수: 이 스크립트가 직접 실행될 때만 handler 함수를 호출합니다.
if __name__ == '__main__':
    print(handler())
