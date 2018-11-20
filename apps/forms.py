class FormMixin(object):
    def get_errors(self):
        # 简化表单错误信息
        if hasattr(self,'errors'):
            errors = self.errors.get_json_data()
            new_errors = {}
            for key,message_dicts in errors.items():
                messages = {}
                for messages in message_dicts:
                    messages.append(messages['message'])
                new_errors[key] = messages
            return new_errors
        else:
            return {}