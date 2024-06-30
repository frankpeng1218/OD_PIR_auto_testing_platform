# Automatic file, do not edit!

class cell():
    def __init__(self, tag, func, paras, default_value = None):
        self.tag = tag
        self.func = func
        # undifined: add nothing
        # []: no parameters
        # [xx, xx]: several parameters
        self.paras = paras
        self.default_value = default_value
        
        self.package_type = None
        self.package = None

        self.data_update_callBack = []        
        self.auto_subscribe_control_flag = True
        self.get_value_called_count = 0
        
        # indicate whether this function has been subscribed
        self.subscribed_flag = False
    
    def update_para(self, para):
        self.paras = para


table_tag = \
{
"be139ea20b00673e9e8dcb7bc1640df9": {"pac": None, "cell": cell("be139ea20b00673e9e8dcb7bc1640df9", "global_objects.speech_recognition_o.set_recognition_url", (), 0)},
"79b023fb7e007b2291a54784c3ab045f": {"pac": None, "cell": cell("79b023fb7e007b2291a54784c3ab045f", "cyberpi.get_mac_address", (), 0)},
"3988e0aab4777855379065fc8da2ba34": {"pac": None, "cell": cell("3988e0aab4777855379065fc8da2ba34", "cyberpi.get_battery", (), 0)},
"86b1f52cbe43f4d01c9c89cda63beb3c": {"pac": None, "cell": cell("86b1f52cbe43f4d01c9c89cda63beb3c", "cyberpi.get_shield", (), 0)},
"e8e71442c9cadf8ca7c89bea4867872c": {"pac": None, "cell": cell("e8e71442c9cadf8ca7c89bea4867872c", "cyberpi.get_extra_battery", (), 0)},
"36a9f3e3395c6747d5b0d3fdde62366d": {"pac": None, "cell": cell("36a9f3e3395c6747d5b0d3fdde62366d", "cyberpi.get_language", (), 0)},
"7801409efa2cbc182d240320f247cf63": {"pac": None, "cell": cell("7801409efa2cbc182d240320f247cf63", "cyberpi.restart", (), 0)},
"6df1c7d3fbdd4da98151197c4825cf2e": {"pac": None, "cell": cell("6df1c7d3fbdd4da98151197c4825cf2e", "cyberpi.is_makex_mode", (), 0)},
"84130d80d8bd240c93e5809565d4fb93": {"pac": None, "cell": cell("84130d80d8bd240c93e5809565d4fb93", "cyberpi.get_firmware_version", (), 0)},
"3636689f7387305b262ef85f68736204": {"pac": None, "cell": cell("3636689f7387305b262ef85f68736204", "cyberpi.get_ble", (), 0)},
"974853ae311b0874fd141e4dbc7ea504": {"pac": None, "cell": cell("974853ae311b0874fd141e4dbc7ea504", "cyberpi.get_name", (), 0)},
"3d43914582aed35b01093bddb465dc5a": {"pac": None, "cell": cell("3d43914582aed35b01093bddb465dc5a", "cyberpi.set_name", (), 0)},
"69d00a7b2ddc1d85e7ed380663f01ecf": {"pac": None, "cell": cell("69d00a7b2ddc1d85e7ed380663f01ecf", "cyberpi.get_brightness", (), 0)},
"04eeffd3a88cf7eee2bf0cb141518cfd": {"pac": None, "cell": cell("04eeffd3a88cf7eee2bf0cb141518cfd", "cyberpi.get_bri", (), 0)},
"2469bdefeb4529102292af589e8a2efc": {"pac": None, "cell": cell("2469bdefeb4529102292af589e8a2efc", "cyberpi.get_loudness", (), 0)},
"4cf92569435ea2828f6e3b6304907430": {"pac": None, "cell": cell("4cf92569435ea2828f6e3b6304907430", "cyberpi.is_tiltback", (), 0)},
"aeefd935140b9ce16ede5da7b7ada9fa": {"pac": None, "cell": cell("aeefd935140b9ce16ede5da7b7ada9fa", "cyberpi.is_tiltforward", (), 0)},
"a4cf641a79cf925a87725098646118f9": {"pac": None, "cell": cell("a4cf641a79cf925a87725098646118f9", "cyberpi.is_tiltleft", (), 0)},
"fec52f5ad18094161cec1b417c7e10f5": {"pac": None, "cell": cell("fec52f5ad18094161cec1b417c7e10f5", "cyberpi.is_tiltright", (), 0)},
"43c455ca4f76e8a737618fbef054bdbe": {"pac": None, "cell": cell("43c455ca4f76e8a737618fbef054bdbe", "cyberpi.is_faceup", (), 0)},
"c6830cf56b1a4f9aaee9ab53e89a923d": {"pac": None, "cell": cell("c6830cf56b1a4f9aaee9ab53e89a923d", "cyberpi.is_facedown", (), 0)},
"c1fb2bd86ac930a853470c2e99c81ea2": {"pac": None, "cell": cell("c1fb2bd86ac930a853470c2e99c81ea2", "cyberpi.is_stand", (), 0)},
"c6d9801ca9be3f1032f2be41538fa658": {"pac": None, "cell": cell("c6d9801ca9be3f1032f2be41538fa658", "cyberpi.is_handstand", (), 0)},
"c33fcd8e57ae1e3b4c513f6f3386b4b6": {"pac": None, "cell": cell("c33fcd8e57ae1e3b4c513f6f3386b4b6", "cyberpi.is_shake", (), 0)},
"e880c1ca448156bf3f371490414e4ee8": {"pac": None, "cell": cell("e880c1ca448156bf3f371490414e4ee8", "cyberpi.is_waveup", (), 0)},
"aefc483bd0bcd4561ee6d6d2abface7c": {"pac": None, "cell": cell("aefc483bd0bcd4561ee6d6d2abface7c", "cyberpi.is_wavedown", (), 0)},
"2dd513e5fbaf94cfe7cafdc64ebbeb74": {"pac": None, "cell": cell("2dd513e5fbaf94cfe7cafdc64ebbeb74", "cyberpi.is_waveleft", (), 0)},
"231b8c48c8b30f532899415153ce868e": {"pac": None, "cell": cell("231b8c48c8b30f532899415153ce868e", "cyberpi.is_waveright", (), 0)},
"dfabbe0e342dffec53fedfff55bff3e1": {"pac": None, "cell": cell("dfabbe0e342dffec53fedfff55bff3e1", "cyberpi.is_freefall", (), 0)},
"fe32241d6feac2a268f7eafa488761eb": {"pac": None, "cell": cell("fe32241d6feac2a268f7eafa488761eb", "cyberpi.is_clockwise", (), 0)},
"196145516d82a638b39657e5b657df7c": {"pac": None, "cell": cell("196145516d82a638b39657e5b657df7c", "cyberpi.is_anticlockwise", (), 0)},
"8a5db13c5c596e0407aa4abbe4f1db48": {"pac": None, "cell": cell("8a5db13c5c596e0407aa4abbe4f1db48", "cyberpi.get_shakeval", (), 0)},
"1632d0eb591aed54c5762a5dcdab81ed": {"pac": None, "cell": cell("1632d0eb591aed54c5762a5dcdab81ed", "cyberpi.get_wave_angle", (), 0)},
"822687ed58d16f303cc79e0b03bb6ce4": {"pac": None, "cell": cell("822687ed58d16f303cc79e0b03bb6ce4", "cyberpi.get_wave_speed", (), 0)},
"1ff145c62ee8412c628e0b0a16fd67fc": {"pac": None, "cell": cell("1ff145c62ee8412c628e0b0a16fd67fc", "cyberpi.get_roll", (), 0)},
"36119451128173ff12497681ec2502e4": {"pac": None, "cell": cell("36119451128173ff12497681ec2502e4", "cyberpi.get_pitch", (), 0)},
"6bc201e4c360195c6ef04a99c3adb982": {"pac": None, "cell": cell("6bc201e4c360195c6ef04a99c3adb982", "cyberpi.get_yaw", (), 0)},
"8f4ae00969ac36f47100a06eee0d5046": {"pac": None, "cell": cell("8f4ae00969ac36f47100a06eee0d5046", "cyberpi.reset_yaw", (), 0)},
"c9f33e1c6b89d173924779a21a9b1019": {"pac": None, "cell": cell("c9f33e1c6b89d173924779a21a9b1019", "cyberpi.get_acc", (), 0)},
"55ddb68e0c157494d0f7e9825815ed43": {"pac": None, "cell": cell("55ddb68e0c157494d0f7e9825815ed43", "cyberpi.get_gyro", (), 0)},
"57f3a0363bf3394221b09dd8c8667892": {"pac": None, "cell": cell("57f3a0363bf3394221b09dd8c8667892", "cyberpi.get_rotation", (), 0)},
"2e150de47aabc09be2cd468491e39a37": {"pac": None, "cell": cell("2e150de47aabc09be2cd468491e39a37", "cyberpi.reset_rotation", (), 0)},
"0f4008600f10c30d9500bf0896cb3945": {"pac": None, "cell": cell("0f4008600f10c30d9500bf0896cb3945", "cyberpi.controller.is_press", (), 0)},
"f57ae52200b5f46041c7804eec7e0423": {"pac": None, "cell": cell("f57ae52200b5f46041c7804eec7e0423", "cyberpi.controller.get_count", (), 0)},
"87aca6f56a1f74eab8abb4c29616ad3c": {"pac": None, "cell": cell("87aca6f56a1f74eab8abb4c29616ad3c", "cyberpi.controller.reset_count", (), 0)},
"99350cd953df88e5f025bcef34113717": {"pac": None, "cell": cell("99350cd953df88e5f025bcef34113717", "cyberpi.audio.play", (), 0)},
"0fd6e3524a5e7c70ccb4ae7194c3ebd4": {"pac": None, "cell": cell("0fd6e3524a5e7c70ccb4ae7194c3ebd4", "cyberpi.audio.play_until", (), 0)},
"8bd7053a4dd190e81637918be72deb46": {"pac": None, "cell": cell("8bd7053a4dd190e81637918be72deb46", "cyberpi.audio.record", (), 0)},
"e5e11eee2dfa73a8626ad875188ce3ca": {"pac": None, "cell": cell("e5e11eee2dfa73a8626ad875188ce3ca", "cyberpi.audio.stop_record", (), 0)},
"7e7984879e15188bbc90283564d6bdf5": {"pac": None, "cell": cell("7e7984879e15188bbc90283564d6bdf5", "cyberpi.audio.play_record_until", (), 0)},
"a8d3656533d5343390a4545985c40c5d": {"pac": None, "cell": cell("a8d3656533d5343390a4545985c40c5d", "cyberpi.audio.play_record", (), 0)},
"611cfa431119957e2345e9db178252c6": {"pac": None, "cell": cell("611cfa431119957e2345e9db178252c6", "cyberpi.audio.play_tone", (), 0)},
"db5f575f0e9b43a42505970665e7f263": {"pac": None, "cell": cell("db5f575f0e9b43a42505970665e7f263", "cyberpi.audio.play_drum", (), 0)},
"3a5b01ef1cc7cf8d5eb05aa275ab0d3f": {"pac": None, "cell": cell("3a5b01ef1cc7cf8d5eb05aa275ab0d3f", "cyberpi.audio.play_music", (), 0)},
"487b1f0a257ab4cad6edd09ea1df35a0": {"pac": None, "cell": cell("487b1f0a257ab4cad6edd09ea1df35a0", "cyberpi.audio.play_note", (), 0)},
"7cf9bc83ad4148ac607d266d30a4d873": {"pac": None, "cell": cell("7cf9bc83ad4148ac607d266d30a4d873", "cyberpi.audio.add_tempo", (), 0)},
"97f80d0c8e36537051d6c9b21e8a7e56": {"pac": None, "cell": cell("97f80d0c8e36537051d6c9b21e8a7e56", "cyberpi.audio.set_tempo", (), 0)},
"0b4dbd2d04bdaac5cf2f578c6087d58d": {"pac": None, "cell": cell("0b4dbd2d04bdaac5cf2f578c6087d58d", "cyberpi.audio.get_tempo", (), 0)},
"f4b0497ab889a85a865a7486dc9c3b20": {"pac": None, "cell": cell("f4b0497ab889a85a865a7486dc9c3b20", "cyberpi.audio.add_vol", (), 0)},
"c2e5e981c561ba61d2d757a61ff17baa": {"pac": None, "cell": cell("c2e5e981c561ba61d2d757a61ff17baa", "cyberpi.audio.set_vol", (), 0)},
"4dedceaadf514a624dea51612e1d3f31": {"pac": None, "cell": cell("4dedceaadf514a624dea51612e1d3f31", "cyberpi.audio.get_vol", (), 0)},
"510b2145fdd0714503879cc98c435d81": {"pac": None, "cell": cell("510b2145fdd0714503879cc98c435d81", "cyberpi.audio.stop", (), 0)},
"3b6fa373ef8ec0614b60949d7a6498eb": {"pac": None, "cell": cell("3b6fa373ef8ec0614b60949d7a6498eb", "cyberpi.display.set_brush", (), 0)},
"f5d5d6501e3af