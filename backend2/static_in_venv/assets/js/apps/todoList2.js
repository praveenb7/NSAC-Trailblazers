$('.input-search').on('keyup', function() {
  var rex = new RegExp($(this).val(), 'i');
    $('.todo-box .todo-item').hide();
    $('.todo-box .todo-item').filter(function() {
        return rex.test($(this).text());
    }).show();
});

const taskViewScroll = new PerfectScrollbar('.task-text', {
    wheelSpeed:.5,
    swipeEasing:!0,
    minScrollbarLength:40,
    maxScrollbarLength:300,
    suppressScrollX : true
});
function dynamicBadgeNotification( setTodoCategoryCount ) {
  var todoCategoryCount = setTodoCategoryCount;

  // Get Parents Div(s)
  var get_ParentsDiv = $('.todo-item');
  var get_TodoAllListParentsDiv = $('.todo-item.all-list');
  var get_TodoCompletedListParentsDiv = $('.todo-item.todo-task-done');
  var get_TodoImportantListParentsDiv = $('.todo-item.todo-task-important');

  // Get Parents Div(s) Counts
  var get_TodoListElementsCount = get_TodoAllListParentsDiv.length;
  var get_CompletedTaskElementsCount = get_TodoCompletedListParentsDiv.length;
  var get_ImportantTaskElementsCount = get_TodoImportantListParentsDiv.length;

  // Get Badge Div(s)
  var getBadgeTodoAllListDiv = $('#all-list .todo-badge');
  var getBadgeCompletedTaskListDiv = $('#todo-task-done .todo-badge');
  var getBadgeImportantTaskListDiv = $('#todo-task-important .todo-badge');


  if (todoCategoryCount === 'allList') {
    if (get_TodoListElementsCount === 0) {
      getBadgeTodoAllListDiv.text('');
      return;
    }
    if (get_TodoListElementsCount > 9) {
        getBadgeTodoAllListDiv.css({
            padding: '2px 0px',
            height: '25px',
            width: '25px'
        });
    } else if (get_TodoListElementsCount <= 9) {
        getBadgeTodoAllListDiv.removeAttr('style');
    }
    getBadgeTodoAllListDiv.text(get_TodoListElementsCount);
  }
  else if (todoCategoryCount === 'completedList') {
    if (get_CompletedTaskElementsCount === 0) {
      getBadgeCompletedTaskListDiv.text('');
      return;
    }
    if (get_CompletedTaskElementsCount > 9) {
        getBadgeCompletedTaskListDiv.css({
            padding: '2px 0px',
            height: '25px',
            width: '25px'
        });
    } else if (get_CompletedTaskElementsCount <= 9) {
        getBadgeCompletedTaskListDiv.removeAttr('style');
    }
    getBadgeCompletedTaskListDiv.text(get_CompletedTaskElementsCount);
  }
  else if (todoCategoryCount === 'importantList') {
    if (get_ImportantTaskElementsCount === 0) {
      getBadgeImportantTaskListDiv.text('');
      return;
    }
    if (get_ImportantTaskElementsCount > 9) {
        getBadgeImportantTaskListDiv.css({
            padding: '2px 0px',
            height: '25px',
            width: '25px'
        });
    } else if (get_ImportantTaskElementsCount <= 9) {
        getBadgeImportantTaskListDiv.removeAttr('style');
    }
    getBadgeImportantTaskListDiv.text(get_ImportantTaskElementsCount);
  }
}

new dynamicBadgeNotification('allList');
new dynamicBadgeNotification('completedList');
new dynamicBadgeNotification('importantList');

/*
  ====================
    Quill Editor
  ====================
*/

var quill = new Quill('#taskdescription', {
  modules: {
    toolbar: [
      [{ header: [1, 2, false] }],
      ['bold', 'italic', 'underline'],
      ['image', 'code-block']
    ]
  },
  placeholder: 'Compose an epic...',
  theme: 'snow'  // or 'bubble'
});

$('#addTaskModal').on('hidden.bs.modal', function (e) {
  // do something...
  $(this)
    .find("input,textarea,select")
       .val('')
       .end();

  quill.deleteText(0, 2000);
})
$('.mail-menu').on('click', function(event) {
  $('.tab-title').addClass('mail-menu-show');
  $('.mail-overlay').addClass('mail-overlay-show');
})
$('.mail-overlay').on('click', function(event) {
  $('.tab-title').removeClass('mail-menu-show');
  $('.mail-overlay').removeClass('mail-overlay-show');
})
$('#addTask').on('click', function(event) {
  event.preventDefault();
  $('.add-tsk').show();
  $('.edit-tsk').hide();
  $('#addTaskModal').modal('show');
  const ps = new PerfectScrollbar('.todo-box-scroll', {
    suppressScrollX : true
  });
});
const ps = new PerfectScrollbar('.todo-box-scroll', {
    suppressScrollX : true
  });

const todoListScroll = new PerfectScrollbar('.todoList-sidebar-scroll', {
    suppressScrollX : true
  });


function todoItem() {
  $('.todo-item .todo-content').on('click', function(event) {
    event.preventDefault();

    var $_taskTitle = $(this).find('.todo-heading').attr('data-todoHeading');
    var $todoHtml = $(this).find('.todo-text').attr('data-todoHtml');

    $('.task-heading').text($_taskTitle);
    $('.task-text').html($todoHtml);

    $('#todoShowListItem').modal('show');
  });
}
var $btns = $('.list-actions').click(function() {
  if (this.id == 'all-list') {
    var $el = $('.' + this.id).fadeIn();
    $('#ct > div').not($el).hide();
  } else if (this.id == 'todo-task-trash') {
    var $el = $('.' + this.id).fadeIn();
    $('#ct > div').not($el).hide();
  } else {
    var $el = $('.' + this.id).fadeIn();
    $('#ct > div').not($el).hide();
  }
  $btns.removeClass('active');
  $(this).addClass('active');
})

checkCheckbox();
deleteDropdown();
deletePermanentlyDropdown();
reviveMailDropdown();
importantDropdown();
priorityDropdown();
editDropdown();
todoItem();

$(".add-tsk").click(function(){
  var today = new Date();
  var dd = String(today.getDate()).padStart(2, '0');
  var mm = String(today.getMonth()); //January is 0!
  var yyyy = today.getFullYear();
  var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ];

  today = monthNames[mm] + ', ' + dd + ' ' + yyyy;
  var $_task = document.getElementById('task').value;

  var $_taskDescriptionText = quill.getText();
  var $_taskDescriptionInnerHTML = quill.root.innerHTML;

  var delta = quill.getContents();
  var $_textDelta = JSON.stringify(delta);

  $html = '<div class="todo-item all-list">'+
              '<div class="todo-item-inner">'+
                  '<div class="n-chk text-center">'+
                      '<label class="new-control new-checkbox checkbox-primary">'+
                        '<input type="checkbox" class="new-control-input inbox-chkbox">'+
                        '<span class="new-control-indicator"></span>'+
                      '</label>'+
                  '</div>'+

                  '<div class="todo-content">'+
                      '<h5 class="todo-heading" data-todoHeading="'+$_task+'"> '+$_task+'</h5>'+
                      '<p class="meta-date">'+today+'</p>'+
                      "<p class='todo-text' data-todoHtml='"+$_taskDescriptionInnerHTML+"' data-todoText='"+$_textDelta+"'> "+$_taskDescriptionText+"</p>"+
                  '</div>'+

                  '<div class="priority-dropdown">'+
                      '<div class="dropdown p-dropdown">'+
                          '<a class="dropdown-toggle primary" href="#" role="button" id="dropdownMenuLink-4" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">'+
                              '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-alert-octagon"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12" y2="16"></line></svg>'+
                          '</a>'+

                          '<div class="dropdown-menu" aria-labelledby="dropdownMenuLink-4">'+
                              '<a class="dropdown-item danger" href="javascript:void(0);"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-alert-octagon"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12" y2="16"></line></svg> High</a>'+
                              '<a class="dropdown-item warning" href="javascript:void(0);"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-alert-octagon"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12" y2="16"></line></svg> Middle</a>'+
                              '<a class="dropdown-item primary" href="javascript:void(0);"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-alert-octagon"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12" y2="16"></line></svg> Low</a>'+
                          '</div>'+
                      '</div>'+
                  '</div>'+

                  '<div class="action-dropdown">'+
                      '<div class="dropdown">'+
                          '<a class="dropdown-toggle" href="#" role="button" id="dropdownMenuLink-4" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">'+
                              '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-more-vertical"><circle cx="12" cy="12" r="1"></circle><circle cx="12" cy="5" r="1"></circle><circle cx="12" cy="19" r="1"></circle></svg>'+
                          '</a>'+

                          '<div class="dropdown-menu" aria-labelledby="dropdownMenuLink-4">'+
                              '<a class="dropdown-item edit" href="javascript:void(0);">Edit</a>'+
                              '<a class="important dropdown-item" href="javascript:void(0);">Important</a>'+
                              '<a class="dropdown-item delete" href="javascript:void(0);">Delete</a>'+
                              '<a class="dropdown-item permanent-delete" href="javascript:void(0);">Permanent Delete</a>'+
                              '<a class="dropdown-item revive" href="javascript:void(0);">Revive Task</a>'+
                          '</div>'+
                      '</div>'+
                  '</div>'+

              '</div>'+
          '</div>';


    $("#ct").prepend($html);
    $('#addTaskModal').modal('hide');
    checkCheckbox();
    deleteDropdown();
    deletePermanentlyDropdown();
    reviveMailDropdown();
    editDropdown();
    priorityDropdown();
    todoItem();
    importantDropdown();
    new dynamicBadgeNotification('allList');
    $(".list-actions#all-list").trigger('click');
});

$('.tab-title .nav-pills a.nav-link').on('click', function(event) {
  $(this).parents('.mail-box-container').find('.tab-title').removeClass('mail-menu-show')
  $(this).parents('.mail-box-container').find('.mail-overlay').removeClass('mail-overlay-show')
})

// Validation Process

  var $_getValidationField = document.getElementsByClassName('validation-text');

  getTaskTitleInput = document.getElementById('task');

  getTaskTitleInput.addEventListener('input', function() {

      getTaskTitleInputValue = this.value;

      if (getTaskTitleInputValue == "") {
        $_getValidationField[0].innerHTML = 'Title Required';
        $_getValidationField[0].style.display = 'block';
      } else {
        $_getValidationField[0].style.display = 'none';
      }
  })

  getTaskDescriptionInput = document.getElementById('taskdescription');

  getTaskDescriptionInput.addEventListener('input', function() {

    getTaskDescriptionInputValue = this.value;

    if (getTaskDescriptionInputValue == "") {
      $_getValidationField[1].innerHTML = 'Description Required';
      $_getValidationField[1].style.display = 'block';
    } else {
      $_getValidationField[1].style.display = 'none';
    }

  })