class all_kinds_of_arguments_i_can_process:
    
    def process_arguments(*args):
        if len(args) == 1:
            code = args[0]
            print(f"Code: {code}")
            return

        code = args[1]
        start_date = None
        end_date = None
        token = None

        for arg in args[2:]:
            if isinstance(arg, str):
                if start_date is None:
                    start_date = arg  # 첫 번째 문자열 인자는 start-date
                elif end_date is None:
                    end_date = arg  # 두 번째 문자열 인자는 end-date
            else:
                token = arg

        print(f"Code: {code}")
        if start_date is not None:
            print(f"Start Date: {start_date}")
        if end_date is not None:
            print(f"End Date: {end_date}")
        if token:
            print(f"Token: {token}")

if __name__ == '__main__':
    dbu = all_kinds_of_arguments_i_can_process()
    dbu.process_arguments("code", "2025-01-01", 123)
