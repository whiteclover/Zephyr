def parse_cmdline():
    cofing = get_file_opt()
    from zephyr.boot import BootOptions
    BootOptions()

    opt, _ = parser.parse_known_args(self.args)
        return opt