document.addEventListener('DOMContentLoaded', function () {
    // 获取所有提问和回答的 div 元素
    const msg_list_ele = document.querySelector('[data-testid="message-list"]')
    const allMessages = document.querySelectorAll('div[data-testid="union_message"]');

    let currentIndex = 0;
    let displayMode = 'all'; // 默认展示所有消息

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
        allMessages[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'end' });
    }

    // 显示下一条消息的函数
    function showNextMessage() {
        if (currentIndex < allMessages.length - 1) {
            currentIndex++;
            const message = allMessages[currentIndex];
            message.style.display = 'block';
            message.classList.add('highlight');

            // 发送消息的内容不逐字打印
            const sendMessageDiv = message.querySelector('div[data-testid="send_message"]');
            if (sendMessageDiv) {
                // 使用整体发送的动态样式
                message.classList.add('send-message-animation');
                setTimeout(() => {
                    message.classList.remove('highlight');
                    message.classList.remove('send-message-animation');
                    message.scrollIntoView({ behavior: 'smooth', block: 'end' });
                }, 1000); // 动画持续时间
                return;
            }

            // 获取消息的原始 HTML 内容
            const originalHTML = message.dataset.originalHtml || message.innerHTML;
            message.dataset.originalHtml = originalHTML;

            // 创建一个临时容器来解析 HTML
            const tempContainer = document.createElement('div');
            tempContainer.innerHTML = originalHTML;

            // 清空消息内容
            message.innerHTML = '';

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

            typeNode(tempContainer, message).then(() => {
                message.classList.remove('highlight');
                message.scrollIntoView({ behavior: 'smooth', block: 'end' });
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
            allMessages[currentIndex].classList.add('highlight');
            const tempIndex = currentIndex;
            setTimeout(() => {
                allMessages[tempIndex].classList.remove('highlight');
            }, 500);
            allMessages[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'end' });
        }
    }

    // 初始化消息显示
    initializeMessages();
    showAllMessages(); // 默认展示所有消息

    // 监听键盘事件
    document.addEventListener('keydown', function (event) {
        switch (event.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                if (displayMode === 'one-by-one') {
                    showNextMessage();
                }
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                if (displayMode === 'one-by-one') {
                    showPreviousMessage();
                }
                break;
            case 'i':
            case 'I':
                displayMode = 'one-by-one';
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