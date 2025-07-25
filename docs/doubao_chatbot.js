document.addEventListener('DOMContentLoaded', function () {
    // 获取所有提问和回答的 div 元素
    const msg_list_ele = document.querySelector('[data-testid="message-list"]');
    const allMessages = Array.from(document.querySelectorAll('div[data-testid="union_message"]')).map(msg => msg.parentNode.parentNode.parentNode);

    let currentIndex = 0;
    let displayMode = 'all'; // 默认展示所有消息

    // 解析 URL 参数
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('dm') === 'i') {
        displayMode = 'interactive'; // 如果 URL 中有 dm=i，则进入交互模式
    }

    // 初始化：隐藏除第一条消息外的所有消息
    function initializeMessages() {
        msg_list_ele.style.flexDirection = 'column-reverse';
        allMessages.forEach((msg, index) => {
            if (index > 0) {
                msg.style.display = 'none';
            } else {
                msg.style.display = 'block';
            }
        });
        currentIndex = 0;
    }

    // 初始化状态变量，用于判断是否正在打印中
    let isTyping = false;

    // 提取 typeNode 函数为独立的异步函数
    async function typeNode(node, target) {
        if (node.nodeType === Node.TEXT_NODE) {
            const text = node.textContent;
            for (let i = 0; i < text.length; i++) {
                await new Promise(resolve => setTimeout(() => {
                    target.appendChild(document.createTextNode(text[i]));
                    resolve();
                }, 10)); // 控制打字速度
            }
        } else if (node.nodeType === Node.ELEMENT_NODE) {
            let clonedElement;
            const tagName = node.tagName.toLowerCase();
            if (['svg', 'path', 'g', 'rect', 'circle', 'line', 'polyline', 'polygon', 'ellipse', 'text', 'tspan', 'use', 'defs', 'clipPath', 'filter', 'mask', 'pattern', 'symbol', 'linearGradient', 'radialGradient', 'stop'].includes(tagName)) {
                // 使用 createElementNS 创建 SVG 元素
                clonedElement = document.createElementNS('http://www.w3.org/2000/svg', node.tagName);
            } else {
                // 使用 createElement 创建普通元素
                clonedElement = document.createElement(node.tagName);
            }

            for (const attr of node.attributes) {
                clonedElement.setAttribute(attr.name, attr.value);
            }
            target.appendChild(clonedElement);

            for (const child of node.childNodes) {
                await typeNode(child, clonedElement);
            }
        }
    }

    // 显示下一条消息的函数
    function showNextMessage() {
        // 如果当前有消息正在打印中，立即完成打印并返回
        if (isTyping && currentIndex < allMessages.length) {
            const currentMessage = allMessages[currentIndex];
            const messageContentDiv = currentMessage.querySelector('div[data-testid="message_content"]');
            if (messageContentDiv) {
                // 立即显示完整内容
                messageContentDiv.innerHTML = messageContentDiv.dataset.originalHtml || messageContentDiv.innerHTML;
                setTimeout(() => {
                    messageContentDiv.classList.remove('highlight');
                }, 300);
                isTyping = false; // 标记打印完成
            }
            return;
        }

        if (currentIndex < allMessages.length - 1) {
            currentIndex++;
            const message = allMessages[currentIndex];
            message.style.display = 'block';
            // messageContentDiv是严格的消息内容div
            const messageContentDiv = message.querySelector('div[data-testid="message_content"]');

            // 发送消息的内容不逐字打印
            const sendMessageDiv = message.querySelector('div[data-testid="send_message"]');
            if (sendMessageDiv) {
                // 使用整体发送的动态样式
                messageContentDiv.classList.add('send-message-animation');
                setTimeout(() => {
                    messageContentDiv.classList.remove('send-message-animation');
                }, 1000); // 动画持续时间
                return;
            }

            messageContentDiv.classList.add('highlight');
            // 获取消息的原始 HTML 内容
            const originalHTML = messageContentDiv.dataset.originalHtml || messageContentDiv.innerHTML;
            messageContentDiv.dataset.originalHtml = originalHTML;

            // 创建一个临时容器来解析 HTML
            const tempContainer = document.createElement('div');
            tempContainer.innerHTML = originalHTML;

            // 清空消息内容
            messageContentDiv.innerHTML = '';

            isTyping = true; // 标记开始打印

            typeNode(tempContainer, messageContentDiv).then(() => {
                setTimeout(() => {
                    messageContentDiv.classList.remove('highlight');
                }, 300);
                isTyping = false; // 标记打印完成
            });
        }
    }

    // 显示所有消息的函数
    function showAllMessages() {
        allMessages.forEach((msg, index) => {
            msg.style.display = 'block';
        });
        msg_list_ele.style.flexDirection = 'column';
    }

    // 显示上一条消息的函数
    function showPreviousMessage() {
        if (currentIndex > 0) {
            allMessages[currentIndex].style.display = 'none';
            currentIndex--;
            allMessages[currentIndex].style.display = 'block';
            const messageContentDiv = allMessages[currentIndex].querySelector('div[data-testid="message_content"]');
            messageContentDiv.classList.add('highlight');
            setTimeout(() => {
                messageContentDiv.classList.remove('highlight');
            }, 500);
        }
    }

    // 初始化消息显示
    if (displayMode === 'interactive') {
        initializeMessages(); // 如果是交互模式，初始化为只显示第一条消息
    } else {
        showAllMessages(); // 默认展示所有消息
    }

    // 监听键盘事件
    document.addEventListener('keydown', function (event) {
        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                if (displayMode === 'interactive') {
                    showNextMessage();
                }
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                if (displayMode === 'interactive') {
                    showPreviousMessage();
                }
                break;
            case 'i':
            case 'I':
                displayMode = 'interactive';
                initializeMessages(); // 重新初始化消息
                break;
            case 'r':
            case 'R':
                displayMode = 'all';
                showAllMessages();
                break;
        }
    });
});