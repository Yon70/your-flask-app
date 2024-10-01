import base64

# 파일 경로
input_file = 'credentials.json'
output_file = 'credentials.b64'

# 파일 읽기
with open(input_file, 'rb') as file:
    file_content = file.read()

# Base64 인코딩
encoded_content = base64.b64encode(file_content).decode('utf-8')

# 인코딩된 내용 파일에 저장
with open(output_file, 'w') as file:
    file.write(encoded_content)

print(f'Encoded content saved to {output_file}')
