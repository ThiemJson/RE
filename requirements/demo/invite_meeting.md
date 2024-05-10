<!-- # REQ-1: Yêu Cầu Đặt Lịch-->
<treqs-element id="c9a45c6e085a11efb56c32bd8644677e" type="requirement">

# REQ-1: Yêu Cầu Đặt Lịch

Hệ thống phải cho phép Người khởi xướng gửi yêu cầu đặt lịch cho Người lập lịch, chỉ rõ khoảng thời gian và người tham gia (`meetingRequest(dateRange, withWhom)`).
</treqs-element>

<!-- 1.1  ## REQ-1.1: Xác Nhận Yêu Cầu -->
<treqs-element id="adc02ab4086411ef8c3432bd8644677e" type="requirement">

## REQ-1.1: Xác Nhận Yêu Cầu

Sau khi nhận được yêu cầu đặt lịch, Người lập lịch phải phản hồi Người khởi xướng xác nhận đã nhận yêu cầu (`OK-request`).
<treqs-link type="parent" target="c9a45c6e085a11efb56c32bd8644677e" />
</treqs-element>

<!-- # REQ-2: Hỏi Điều Kiện -->
<treqs-element id="f81e9b0e086411efbe2a32bd8644677e" type="requirement">

# REQ-2: Hỏi Điều Kiện

Người lập lịch phải truy vấn Người tham gia về bất kỳ ràng buộc nào liên quan đến cuộc họp được đề xuất (`? constraints`).
</treqs-element>

<!-- ## REQ-2.1: Cung Cấp Ràng Buộc -->
<treqs-element id="522e2924086611ef95ed32bd8644677e" type="requirement">

## REQ-2.1: Cung Cấp Ràng Buộc

Người tham gia phải cung cấp các ràng buộc cho Người lập lịch, có thể bao gồm các khung giờ có thể hoặc các điều kiện khác (`! constraints`).
<treqs-link type="parent" target="f81e9b0e086411efbe2a32bd8644677e" />
</treqs-element>

<!-- # REQ-3: Xác Nhận Ràng Buộc -->
<treqs-element id="57770870086511efb70632bd8644677e" type="requirement">

# REQ-3: Xác Nhận Ràng Buộc

Sau khi nhận và xử lý các ràng buộc, Người lập lịch phải xác nhận lại những ràng buộc này với Người tham gia (`OK-constr`).
</treqs-element>

<!-- # REQ-4: Xác Định Lịch Trình -->
<treqs-element id="5c3f188e086511efaedb32bd8644677e" type="requirement">

# REQ-4: Xác Định Lịch Trình

Người tham gia, sau khi đồng ý hoặc điều chỉnh các ràng buộc, phải xác định lịch trình cuối cùng (`scheduleDetermination`) và thông báo cho Người lập lịch.
</treqs-element>

<!-- # REQ-5: Thông Báo Cuộc Họp -->
<treqs-element id="5f85e73e086511efb56432bd8644677e" type="requirement">

# REQ-5: Thông Báo Cuộc Họp

Người lập lịch phải thông báo cho cả Người tham gia và Người khởi xướng về ngày giờ và địa điểm cuộc họp cuối cùng (`notification(date, location)`).
</treqs-element>

<!-- # REQ-5: Thông Báo Cuộc Họp -->
<treqs-element id="9c3807c00ec811ef95d5985aeb8b59b0" type="requirement">

# REQ-6: Thông Báo Cuộc Họp ketthuc

Người lập lịch phải thông báo cho cả Người tham gia và Người khởi xướng về ngày giờ và địa điểm cuộc họp cuối cùng (`notification(date, location)`).
</treqs-element>

<treqs-element id="8dd284e4513c11ed97c08adebfb72d7e22222" type="information">

### Bieu Do UML

<!--
@startuml invite_meeting
participant Initiator
participant Scheduler
participant Participant

Initiator -> Scheduler : meetingRequest(dateRange, withWhom)
Scheduler -> Initiator : OK-request

Scheduler -> Participant : ? constraints
Participant -> Scheduler : ! constraints

Scheduler -> Participant : OK-constr

Participant -> Scheduler : scheduleDetermination
Scheduler -> Participant : notification(date, location)
Participant -> Initiator : notification(date, location)

@enduml
-->

![treqs create details](invite_meeting.png)
</treqs-element>
