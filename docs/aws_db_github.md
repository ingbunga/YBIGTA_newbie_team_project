

# 비공개 설정 & 로드밸런서 구성

[클라이언트] → 80포트 → [AWS ALB] → 8000포트 → [EC2 FastAPI]


## 1. RDS 비공개 설정 (퍼블릭 액세스 차단)

### 구성 개요
- RDS 생성 시 `Public Access = No`로 설정하여 외부 인터넷에서 직접 접속 불가
- EC2와 RDS를 **동일한 VPC**에 배치해 내부 IP로만 통신
- 보안 그룹에서 **MySQL(3306)** 포트를 EC2 보안 그룹만 허용

### 설정 효과
- DB 엔드포인트가 외부에 노출되지 않아 보안 강화
- 오직 EC2를 거쳐서만 RDS 접근 가능

### 설정

![rds setting](/aws/rds-setting.png)


---

## 2. 로드밸런서를 통한 포트 비공개 설정

### 구성 개요
- 외부 사용자는 HTTP 80 포트(로드밸런서)로만 접근 가능
- 로드밸런서가 Target Group을 통해 내부적으로 EC2의 8000 포트로 요청 전달
- EC2 8000 포트는 로드밸런서 보안 그룹만 접근 가능
- Target Group Health Check Path를 `/health`로 설정하여 정상 상태 확인

### 헬스 체크 엔드포인트 코드
`/app/app/main.py`
```python
app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```



### 경로 /health로 설정하여 로드밸런서가 서버가 살아 있는지 주기적으로 확인할 때 http://<서버주소>/health 경로로 요청을 보내도록 설정
![load balancer health check](/aws/loadbalancer-healthcheck.png)


### 리스너 설정
![load balancer listener](/aws/loadbalancer-listener.png)


### 대상 설정
![load balancer target](/aws/loadbalancer-target.png)

### 로드밸런서 통해 문서 접속
![load balancer web page](/aws/loadbalancer-web.png)


# Github Action 캡쳐
![github action](/aws/github_action.png)


# SWAGGER 캡쳐

## 1. Health Check API
**URL:** `GET /health`
![health check](/aws/health.png)

## 2. User Login API
**URL:** `POST /api/user/login`
![login](/aws/login.png)

## 3. User Registration API
**URL:** `POST /api/user/register`
![register](/aws/register.png)

## 4. User Delete API
**URL:** `DELETE /api/user/delete`
![delete](/aws/delete.png)

## 5. User Update Password API
**URL:** `PUT /api/user/update-password`
![update password](/aws/update-password.png)

## 6. Review Preprocess API
**URL:** `POST /review/preprocess/{site_name}`
![preprocess](/aws/preprocess.png)

## 7. Get Preprocessed Reviews API
**URL:** `GET /review/preprocessed/{id}`
![preprocessed](/aws/preprocessed.png)



