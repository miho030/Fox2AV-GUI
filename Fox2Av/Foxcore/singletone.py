class InfectionRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InfectionRegistry, cls).__new__(cls)
            cls._instance.infections = []  # 감염된 파일 정보 리스트
        return cls._instance

    def add_infection(self, file_path, file_name, file_hash):
        # 파일 경로, 파일 이름, 파일 해시값을 함께 저장 (튜플로 저장)
        self.infections.append((file_path, file_name, file_hash))

    def get_infections(self):
        return self.infections

# 싱글톤 인스턴스 생성
infection_registry = InfectionRegistry()