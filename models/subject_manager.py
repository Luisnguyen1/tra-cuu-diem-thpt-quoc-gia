class Subject:
    def __init__(self, code, name):
        self.code = code  # Mã môn trong DB (vd: toan, ngu_van)
        self.name = name  # Tên hiển thị (vd: Toán, Ngữ Văn)

class Block:
    def __init__(self, code, subjects, description=None):
        self.code = code  # Mã khối (vd: A00, B00)
        self.subjects = subjects  # List các Subject
        self.description = description  # Mô tả thêm về khối

    @property
    def display_name(self):
        """Tạo tên hiển thị cho khối"""
        subject_names = ' - '.join(subject.name for subject in self.subjects)
        return f"{self.code}: {subject_names}"

    def get_subject_codes(self):
        """Lấy danh sách mã môn học trong khối"""
        return [subject.code for subject in self.subjects]

class SubjectManager:
    def __init__(self):
        self.subjects = {}  # Dictionary chứa tất cả các môn học
        self.blocks = {}    # Dictionary chứa tất cả các khối
        self._init_subjects()
        self._init_blocks()

    def _init_subjects(self):
        """Khởi tạo danh sách môn học"""
        subject_data = {
            'toan': 'Toán',
            'ngu_van': 'Ngữ Văn',
            'ngoai_ngu': 'Tiếng Anh',
            'vat_li': 'Vật lí',
            'hoa_hoc': 'Hóa học',
            'sinh_hoc': 'Sinh học',
            'lich_su': 'Lịch sử',
            'dia_li': 'Địa lí',
            'gdcd': 'Giáo dục công dân'
        }
        for code, name in subject_data.items():
            self.subjects[code] = Subject(code, name)

    def _init_blocks(self):
        """Khởi tạo danh sách khối thi"""
        # Khối A
        self._add_block('A00', ['toan', 'vat_li', 'hoa_hoc'])
        self._add_block('A01', ['toan', 'vat_li', 'ngoai_ngu'])
        self._add_block('A02', ['toan', 'vat_li', 'sinh_hoc'])
        self._add_block('A03', ['toan', 'vat_li', 'lich_su'])
        self._add_block('A04', ['toan', 'vat_li', 'dia_li'])
        self._add_block('A05', ['toan', 'hoa_hoc', 'lich_su'])
        self._add_block('A06', ['toan', 'hoa_hoc', 'dia_li'])
        self._add_block('A07', ['toan', 'lich_su', 'dia_li'])
        self._add_block('A08', ['toan', 'lich_su', 'gdcd'])
        self._add_block('A09', ['toan', 'dia_li', 'gdcd'])
        self._add_block('A10', ['toan', 'vat_li', 'gdcd'])
        self._add_block('A11', ['toan', 'hoa_hoc', 'gdcd'])

        # Khối B
        self._add_block('B00', ['toan', 'hoa_hoc', 'sinh_hoc'])
        self._add_block('B01', ['toan', 'sinh_hoc', 'lich_su'])
        self._add_block('B02', ['toan', 'sinh_hoc', 'dia_li'])
        self._add_block('B03', ['toan', 'sinh_hoc', 'ngu_van'])
        self._add_block('B04', ['toan', 'sinh_hoc', 'gdcd'])
        self._add_block('B08', ['toan', 'sinh_hoc', 'ngoai_ngu'])

        # Khối C
        self._add_block('C00', ['ngu_van', 'lich_su', 'dia_li'])
        self._add_block('C01', ['ngu_van', 'toan', 'vat_li'])
        self._add_block('C02', ['ngu_van', 'toan', 'hoa_hoc'])
        self._add_block('C03', ['ngu_van', 'toan', 'lich_su'])
        self._add_block('C04', ['ngu_van', 'toan', 'dia_li'])
        self._add_block('C05', ['ngu_van', 'vat_li', 'hoa_hoc'])
        self._add_block('C06', ['ngu_van', 'vat_li', 'sinh_hoc'])
        self._add_block('C07', ['ngu_van', 'vat_li', 'lich_su'])
        self._add_block('C08', ['ngu_van', 'hoa_hoc', 'sinh_hoc'])
        self._add_block('C09', ['ngu_van', 'vat_li', 'dia_li'])
        self._add_block('C10', ['ngu_van', 'hoa_hoc', 'lich_su'])
        self._add_block('C12', ['ngu_van', 'sinh_hoc', 'lich_su'])
        self._add_block('C13', ['ngu_van', 'sinh_hoc', 'dia_li'])
        self._add_block('C14', ['ngu_van', 'toan', 'gdcd'])
        self._add_block('C16', ['ngu_van', 'vat_li', 'gdcd'])
        self._add_block('C17', ['ngu_van', 'hoa_hoc', 'gdcd'])
        self._add_block('C19', ['ngu_van', 'lich_su', 'gdcd'])
        self._add_block('C20', ['ngu_van', 'dia_li', 'gdcd'])

        # Khối D
        self._add_block('D01', ['ngu_van', 'toan', 'ngoai_ngu'])
        self._add_block('D07', ['toan', 'hoa_hoc', 'ngoai_ngu'])
        self._add_block('D08', ['toan', 'sinh_hoc', 'ngoai_ngu'])
        self._add_block('D09', ['toan', 'lich_su', 'ngoai_ngu'])
        self._add_block('D10', ['toan', 'dia_li', 'ngoai_ngu'])
        self._add_block('D11', ['ngu_van', 'vat_li', 'ngoai_ngu'])
        self._add_block('D12', ['ngu_van', 'hoa_hoc', 'ngoai_ngu'])
        self._add_block('D13', ['ngu_van', 'sinh_hoc', 'ngoai_ngu'])
        self._add_block('D14', ['ngu_van', 'lich_su', 'ngoai_ngu'])
        self._add_block('D15', ['ngu_van', 'dia_li', 'ngoai_ngu'])

    def _add_block(self, code, subject_codes, description=None):
        """Helper method để thêm một khối mới"""
        subjects = [self.subjects[code] for code in subject_codes]
        self.blocks[code] = Block(code, subjects, description)

    def get_block(self, code):
        """Lấy thông tin một khối theo mã"""
        return self.blocks.get(code)

    def get_all_blocks(self):
        """Lấy thông tin tất cả các khối"""
        return self.blocks

    def get_block_subjects(self, block_code):
        """Lấy danh sách môn học của một khối"""
        block = self.blocks.get(block_code)
        return block.get_subject_codes() if block else []

    def get_subject_name(self, code):
        """Lấy tên hiển thị của một môn học"""
        subject = self.subjects.get(code)
        return subject.name if subject else code

    def get_blocks_for_display(self):
        """Lấy thông tin các khối để hiển thị trong UI"""
        return {code: block.display_name for code, block in self.blocks.items()} 