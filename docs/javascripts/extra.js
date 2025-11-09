// Elegant footer styling and image modal functionality
document.addEventListener('DOMContentLoaded', function() {
    // Replace copyright content with links
    const copyrightElement = document.querySelector('.md-copyright__highlight');
    if (copyrightElement) {
        copyrightElement.innerHTML = `
            Copyright © 2025 射频细胞 | 美的觉醒 | 
            <a href="https://beian.miit.gov.cn/" target="_blank">京 ICP 备 20009050 号-3</a> | 
            联系信息：<a href="mailto:yuxiaodong@beaucare.org">yuxiaodong@beaucare.org</a> @sooogooo
        `;
        
        copyrightElement.style.cssText = `
            display: block !important;
            visibility: visible !important;
            color: #666666 !important;
            font-size: 0.7rem !important;
            opacity: 0.8 !important;
            font-weight: 400 !important;
            text-align: left !important;
            padding: 1rem 1.2rem !important;
            line-height: 1.6 !important;
            background: transparent !important;
            border: none !important;
            margin: 0 !important;
        `;
    }
    
    // Remove "Made with" section
    const madeWithElements = document.querySelectorAll('.md-copyright > *:not(.md-copyright__highlight)');
    madeWithElements.forEach(element => {
        if (element.textContent.includes('Made with') || element.textContent.includes('Material for MkDocs')) {
            element.style.display = 'none !important';
        }
    });
    
    // Style the entire copyright section
    const copyrightSection = document.querySelector('.md-copyright');
    if (copyrightSection) {
        copyrightSection.style.cssText = `
            background-color: #fafafa !important;
            padding: 0 !important;
            margin: 0 !important;
            border-top: 1px solid #e0e0e0 !important;
        `;
    }
    
    // Style the footer meta section
    const footerMeta = document.querySelector('.md-footer-meta');
    if (footerMeta) {
        footerMeta.style.cssText = `
            background-color: #fafafa !important;
            border-top: 1px solid #e0e0e0 !important;
            padding: 0 !important;
        `;
    }
    
    // Style links in footer
    const footerLinks = document.querySelectorAll('.md-copyright a');
    footerLinks.forEach(link => {
        link.style.cssText = `
            color: #0066cc !important;
            text-decoration: none !important;
            opacity: 0.8 !important;
            transition: opacity 0.2s ease !important;
        `;
        
        link.addEventListener('mouseenter', function() {
            this.style.opacity = '1 !important';
            this.style.textDecoration = 'underline !important';
        });
        
        link.addEventListener('mouseleave', function() {
            this.style.opacity = '0.8 !important';
            this.style.textDecoration = 'none !important';
        });
    });
    
    // Image modal functionality for enhanced image viewing
    createImageModal();
});

function createImageModal() {
    // Create modal element
    const modal = document.createElement('div');
    modal.id = 'imageModal';
    modal.style.cssText = `
        display: none;
        position: fixed;
        z-index: 10000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.9);
        backdrop-filter: blur(5px);
        cursor: zoom-out;
        animation: fadeIn 0.3s ease;
    `;
    
    // Create modal content
    const modalContent = document.createElement('img');
    modalContent.id = 'modalImage';
    modalContent.style.cssText = `
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        max-width: 90%;
        max-height: 90%;
        object-fit: contain;
        border-radius: 8px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
        transition: transform 0.3s ease;
        cursor: grab;
    `;
    
    // Create caption
    const caption = document.createElement('div');
    caption.id = 'modalCaption';
    caption.style.cssText = `
        position: absolute;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        color: white;
        font-size: 16px;
        text-align: center;
        background: rgba(0, 0, 0, 0.7);
        padding: 8px 16px;
        border-radius: 20px;
        backdrop-filter: blur(10px);
    `;
    
    // Create close button
    const closeBtn = document.createElement('span');
    closeBtn.innerHTML = '×';
    closeBtn.style.cssText = `
        position: absolute;
        top: 20px;
        right: 30px;
        color: white;
        font-size: 40px;
        font-weight: bold;
        cursor: pointer;
        transition: color 0.3s ease;
    `;
    
    closeBtn.addEventListener('mouseenter', function() {
        this.style.color = '#ff6b6b';
    });
    
    closeBtn.addEventListener('mouseleave', function() {
        this.style.color = 'white';
    });
    
    // Create zoom controls
    const zoomControls = document.createElement('div');
    zoomControls.style.cssText = `
        position: absolute;
        top: 20px;
        left: 20px;
        display: flex;
        flex-direction: column;
        gap: 10px;
    `;
    
    const zoomInBtn = document.createElement('button');
    zoomInBtn.innerHTML = '+';
    zoomInBtn.style.cssText = `
        width: 40px;
        height: 40px;
        border: none;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        font-size: 20px;
        cursor: pointer;
        transition: background 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    const zoomOutBtn = document.createElement('button');
    zoomOutBtn.innerHTML = '−';
    zoomOutBtn.style.cssText = `
        width: 40px;
        height: 40px;
        border: none;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        font-size: 20px;
        cursor: pointer;
        transition: background 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    const resetBtn = document.createElement('button');
    resetBtn.innerHTML = '⟲';
    resetBtn.style.cssText = `
        width: 40px;
        height: 40px;
        border: none;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.2);
        color: white;
        font-size: 16px;
        cursor: pointer;
        transition: background 0.3s ease;
        backdrop-filter: blur(10px);
    `;
    
    // Add hover effects for buttons
    [zoomInBtn, zoomOutBtn, resetBtn].forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(255, 255, 255, 0.3)';
        });
        btn.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.2)';
        });
    });
    
    modal.appendChild(modalContent);
    modal.appendChild(caption);
    modal.appendChild(closeBtn);
    zoomControls.appendChild(zoomInBtn);
    zoomControls.appendChild(zoomOutBtn);
    zoomControls.appendChild(resetBtn);
    modal.appendChild(zoomControls);
    document.body.appendChild(modal);
    
    // Add CSS animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        .modal-fade-out {
            animation: fadeOut 0.3s ease;
        }
    `;
    document.head.appendChild(style);
    
    let currentScale = 1;
    let isDragging = false;
    let startX, startY, startScrollLeft, startScrollTop;
    
    // Modal functionality
    function openModal(img) {
        modal.style.display = 'block';
        modalContent.src = img.src;
        modalContent.alt = img.alt;
        caption.textContent = img.alt || '';
        currentScale = 1;
        updateTransform();
        document.body.style.overflow = 'hidden';
    }
    
    function closeModal() {
        modal.classList.add('modal-fade-out');
        setTimeout(() => {
            modal.style.display = 'none';
            modal.classList.remove('modal-fade-out');
            document.body.style.overflow = 'auto';
            currentScale = 1;
            updateTransform();
        }, 300);
    }
    
    function updateTransform() {
        modalContent.style.transform = `translate(-50%, -50%) scale(${currentScale})`;
    }
    
    // Event listeners
    closeBtn.addEventListener('click', closeModal);
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    zoomInBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        currentScale = Math.min(currentScale * 1.2, 3);
        updateTransform();
    });
    
    zoomOutBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        currentScale = Math.max(currentScale / 1.2, 0.5);
        updateTransform();
    });
    
    resetBtn.addEventListener('click', function(e) {
        e.stopPropagation();
        currentScale = 1;
        updateTransform();
    });
    
    // Keyboard controls
    document.addEventListener('keydown', function(e) {
        if (modal.style.display === 'block') {
            if (e.key === 'Escape') {
                closeModal();
            } else if (e.key === '+' || e.key === '=') {
                currentScale = Math.min(currentScale * 1.1, 3);
                updateTransform();
            } else if (e.key === '-' || e.key === '_') {
                currentScale = Math.max(currentScale / 1.1, 0.5);
                updateTransform();
            }
        }
    });
    
    // Mouse wheel zoom
    modal.addEventListener('wheel', function(e) {
        if (e.ctrlKey) {
            e.preventDefault();
            const delta = e.deltaY > 0 ? 0.9 : 1.1;
            currentScale = Math.max(0.5, Math.min(3, currentScale * delta));
            updateTransform();
        }
    });
    
    // Apply to images with specific class or all images in main content
    const mainImages = document.querySelectorAll('img[src*="images/visuals/"]');
    mainImages.forEach(img => {
        img.style.cursor = 'zoom-in';
        img.style.transition = 'transform 0.3s ease';
        
        img.addEventListener('click', function(e) {
            e.preventDefault();
            openModal(this);
        });
        
        // Add hover effect
        img.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
        });
        
        img.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}