from email import message
import base64

class BulkMailService:
    def __init__(self, sender = None, mail_service = None) -> None:
        self.msg = message.EmailMessage()
        self.sender = sender
        self.receiver = []
        self.attachment_path = None
        self.subject = ''
        self.body = ''
        self.email_service = mail_service
        self.check_berfore_send = True

    def __str__(self):
        return f'''
        Sender: {self.sender}
        Receiver: {self.receiver}
        Subject: {self.subject}
        Attachment: {self.attachment_path}
        '''

    def _message(self):
        self.msg["From"] = self.sender
        self.msg["To"] = ','.join(self.receiver)
        self.msg["subject"] = self.subject
        self.msg.add_alternative(self.body,subtype="html")

        if self.attachment_path:
            with open(self.attachment_path, 'rb') as fp:
                attachment_data = fp.read()
                file_name = self.attachment_path.split('/')[-1]
                file_type = self.attachment_path.split('.')[-1]
                self.msg.add_attachment(attachment_data, \
                    maintype="application", \
                    subtype = file_type, \
                    filename = file_name)
        return self.msg

    def preview(self):
        print(self.msg)

    def send(self):
        assert self.receiver, '收件人未填'

        message = self._message()
        raw_message = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        if self.check_berfore_send:
            self.preview()
            cancel = input("Press Enter to send the email, type anything to cancel.")
        if cancel:
            return 'Email sending cancelled.'
        try:
            result = self.email_service.users().messages().send(userId='me', body=raw_message).execute()
            print("Email sent successfully using Gmail API.")
        except Exception as e:
            print(f"An error occurred while sending email: {e}")

        return result