hello-user = Привет, { $username }. Нажмите на кнопку

button-button = Кнопка

button-pressed = Вы нажали на кнопку

no-copy = Данный тип апдейтов не поддерживается методом send_copy

send-text = Отправьте любой текст, который необходимо сохранить в FSM-хранилище NATS

successfully-saved = Ваш текст успешно сохранен в NATS FSM-storage

                     Теперь вы можете получить данные из хранилища, отправив команду /read.

text-only = Пожалуйста, отправляйте только текстовые сообщения

will-delete = Это сообщение удалится через { $delay ->
                [one] { $delay } секунду
                [few] { $delay } секунды
               *[other] { $delay } секунд
              }