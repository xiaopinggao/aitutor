document.addEventListener('DOMContentLoaded', function () {
    // 获取所有提问和回答的 div 元素
    const allMessages = document.querySelectorAll('.container-ncFTrL');

    let currentIndex = 0;

    // 初始化：隐藏除第一条消息外的所有消息
    function initializeMessages() {
        allMessages.forEach((msg, index) => {
            if (index > 0) {
                msg.style.display = 'none';
            } else {
                msg.style.display = 'block';
            }
        });
        currentIndex = 0;
        allMessages[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    // 显示下一条消息的函数
    function showNextMessage() {
        if (currentIndex < allMessages.length - 1) {
            currentIndex++;
            allMessages[currentIndex].style.display = 'block';
            allMessages[currentIndex].classList.add('highlight');
            const tempIndex = currentIndex;
            setTimeout(() => {
                allMessages[tempIndex].classList.remove('highlight');
            }, 500);
            allMessages[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    }

    // 显示上一条消息的函数
    function showPreviousMessage() {
        if (currentIndex > 0) {
            allMessages[currentIndex].style.display = 'none';
            currentIndex--;
            allMessages[currentIndex].style.display = 'block';
            allMessages[currentIndex].classList.add('highlight');
            const tempIndex = currentIndex;
            setTimeout(() => {
                allMessages[tempIndex].classList.remove('highlight');
            }, 500);
            allMessages[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    }

    // 重启对话，回到初始状态的函数
    function restartConversation() {
        initializeMessages();
    }

    // 初始化消息显示
    initializeMessages();

    // 监听键盘事件
    document.addEventListener('keydown', function (event) {
        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                showNextMessage();
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                showPreviousMessage();
                break;
            case 'r':
            case 'R':
                restartConversation();
                break;
        }
    });

    // 监听鼠标事件
    document.addEventListener('mousedown', function (event) {
        if (event.button === 0) { // 左键
            showNextMessage();
        }
    });
});