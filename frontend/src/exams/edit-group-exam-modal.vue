<template>
  <b-modal v-model="modalVisible"
           :no-close-on-backdrop="true"
           hide-header
           @shown="show"
           hide-footer
           size="md">
    <div v-if="showModal">
      <span class="q-modal-header">Edit {{ titleText }} Exam Booking</span>
      <b-form autocomplete="off">
        <b-form-row>
          <b-col class="mb-2">
            <div class="q-info-display-grid-container">
              <div class="q-id-grid-outer">
                <div class="q-id-grid-head">Exam Details</div>
                <div class="q-id-grid-col">
                  <div>Exam: </div>
                  <div>{{ actionedExam.exam_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Event ID: </div>
                  <div>{{ actionedExam.event_id }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Type: </div>
                  <div>{{ actionedExam.exam_type.exam_type_name }}</div>
                </div>
                <div class="q-id-grid-col">
                  <div>Writers: </div>
                  <div>{{ actionedExam.number_of_students }}</div>
                </div>
                <div class="q-id-grid-col" v-if="is_liaison_designate">
                  <div>Office: </div>
                  <div>{{ actionedExam.office.office_name }}</div>
                </div>
              </div>
            </div>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col cols="6">
            <b-form-group>
              <label>Exam Date</label><br>
              <DatePicker :value="date"
                          style="color: black"
                          :disabled="fieldDisabled"
                          name="date"
                          input-class="custom-disabled-fields form-control"
                          class="w-100 date-time-fields"
                          @input="checkDate"
                          lang="en">
              </DatePicker>
            </b-form-group>
          </b-col>

          <b-col cols="6">
            <b-form-group>
              <label>Exam Time</label><br>
              <DatePicker v-model="time"
                          class="w-100"
                          :disabled="fieldDisabled"
                          :time-picker-options="{ start: '8:00', step: '00:30', end: '17:00' }"
                          lang="en"
                          format="h:mm a"
                          input-class="custom-disabled-fields form-control"
                          name="time"
                          @input="checkTime"
                          type="time">
                <template slot="calendar-icon">
                  <font-awesome-icon icon="clock"
                                     class="m-0 p-0"
                                     style="font-size: .9rem;"/>
                </template>
              </DatePicker>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <b-col>
            <b-form-group>
              <label>Location</label><br>
              <b-textarea v-model="offsite_location"
                          :disabled="fieldDisabled"
                          style="color: #525252"
                          class="mb-0 custom-disabled-fields"
                          :rows="2"
                          name="offsite_location"
                          @input.native="checkInput" />
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row align-content="end" align-h="end" class="w-100">
          <b-col :cols="is_liaison_designate || role_code === 'GA' ? 10 : '' ">
            <b-form-group>
              <label>Invigilator</label><br>
              <b-select v-model="invigilator_id"
                        name="invigilator_id"
                        @change.native="checkInput"
                        :options="invigilator_dropdown"/>
            </b-form-group>
          </b-col>
        </b-form-row>
        <b-form-row>
          <template v-if="this.currentShadowInvigilator != null">
            <b-row style="display: flex;" class="w-100 ml-0 mb-2">
              <b-col class="w-50 ml-1 mr-1 pr-1">
                <b-button v-if="this.changeState"
                          v-b-toggle.collapse-1
                          variant="primary"
                          @click="setRemove">
                  Change Shadow Invigilator
                </b-button>
                <b-button v-else-if="!this.changeState"
                          disabled
                          variant="primary">
                  Change Shadow Invigilator
                </b-button>
              </b-col>
              <b-col class="w-50 ml-1 mr-1 pl-1">
                <b-button v-if="this.removeState"
                          v-b-toggle.collapse-2
                          variant="danger"
                          @click="setChange">
                  Remove Shadow Invigilator
                </b-button>
                <b-button v-else-if="!this.removeState"
                          disabled
                          variant="danger">
                  Remove Shadow Invigilator
                </b-button>
              </b-col>
            </b-row>
          </template>
          <template v-else>
            <b-button v-b-toggle.collapse-1
                    variant="primary"
                    class="w-100 m-1">
              Add Shadow Invigilator
            </b-button>
          </template>
          <b-collapse id="collapse-1"
                      class="mt-2 mb-2 w-100">
            <b-form-group class="q-info-display-grid-container">
              <label>Shadow Invigilators</label>
              <b-form>
                <b-row>
                  <b-col>
                    <b-table selectable
                             select-mode="single"
                             :fields="shadowFields"
                             :items="shadow_invigilator_options"
                             @row-selected="rowSelectedShadow"
                             responsive
                             selected-variant="success"
                             style="height: 100px;"
                             bordered
                             striped>
                      <template slot="selected" slot-scope=" { rowSelected } ">
                        <span v-if="rowSelected">✔</span>
                      </template>
                    </b-table>
                  </b-col>
                  <b-col>
                    <b-row>
                      Shadow Invigilator Limit: 1
                    </b-row>
                    <b-row v-if="this.currentShadowInvigilator != null"
                           class="mb-1">
                      Current Invigilator
                    </b-row>
                    <b-row v-if="this.currentShadowInvigilator != null"
                           style="justify-content: center;"
                           class="mb-1">
                      {{ this.currentShadowInvigilatorName }}
                    </b-row>
                    <b-row style="font-weight: bold;"
                           class="mb-0">
                      Selected Invigilators
                    </b-row>
                    <b-row v-for="select in selectedShadow"
                           style="justify-content: center;"
                           class="mb-0">
                      {{ select.name }}
                    </b-row>
                  </b-col>
                </b-row>
              </b-form>
            </b-form-group>
          </b-collapse>
          <b-collapse id="collapse-2"
                      class="mt-2 w-100">
            <b-form-group class="q-info-display-grid-container">
              <b-row class="ml-1">
                <span style="font-weight: bold;">Current Shadow Invigilator: </span>
              </b-row>
              <b-row class="mb-2"
                     style="justify-content: center;">
                <span>{{ this.currentShadowInvigilatorName}}</span>
              </b-row>
              <b-row class="ml-1">
                <span style="font-weight: bold;">Would you like to remove this shadow invigilator?</span>
              </b-row>
              <template>
                <b-row style="display: flex; justify-content: center;"
                       class="w-100 mb-0">
                  <b-button class="mr-2 mt-1"
                            variant="danger"
                            @click="setSelectedShadowNull">
                    Yes
                  </b-button>
                  <b-button class="ml-2 mt-1"
                            variant="primary"
                            v-b-toggle.collapse-2
                            @click="setChange">
                    No
                  </b-button>
                </b-row>
              </template>
            </b-form-group>
          </b-collapse>
        </b-form-row>
      </b-form>
      <div v-if="showMessage"
            class="mb-3"
            style="color: red;">Nothing has changed.  All fields contain their initial values.</div>
      <div style="display: flex; justify-content: flex-end; width: 100%" class="mt-2">
        <b-btn class="btn-secondary mr-2" @click="cancel">Cancel</b-btn>
        <b-btn v-if="!allowSubmit"
               class="btn-primary disabled"
               @click="showMessage=true">Submit</b-btn>
        <b-btn v-else-if="allowSubmit"
               class="btn-primary"
               @click="submit">Submit</b-btn>
        <b-btn variant="warning"
               @click="show"
               class="ml-2">Reset Form</b-btn>
      </div>
    </div>
  </b-modal>
</template>

<script>
  import { mapActions, mapMutations, mapState, mapGetters } from 'vuex'
  import moment from 'moment'
  import zone from 'moment-timezone'
  import DatePicker from 'vue2-datepicker'
  export default {
    name: "EditGroupExamBookingModal",
    components: { DatePicker },
    props: ['actionedExam', 'resetExam'],
    data () {
      return {
        invigilator_id: '',
        date: '',
        time: '',
        offsite_location: '',
        editedFields: [],
        showMessage: false,
        itemCopy: {},
        currentShadowInvigilator: null,
        currentShadowInvigilatorName: '',
        shadowInvigilator: null,
        selectedShadow: [],
        shadowFields: ['selected', 'name'],
        changeState: true,
        removeState: true,
        removeFlag: false,
      }
    },
    computed: {
      ...mapGetters(['role_code',
                     'invigilator_dropdown',
                     'is_liaison_designate',
                     'shadow_invigilator_options',]),
      ...mapState({
        showModal: state => state.showEditGroupBookingModal,
        invigilators: 'invigilators',
        user: 'user',
        shadowInvigilators: state => state.shadowInvigilators,
      }),
      allowSubmit() {
        if (!this.editedFields || this.editedFields.length === 0) {
          return false
        }
        if (this.actionedExam.offsite_location === '_offsite') {
          if (this.editedFields.length >= 3 && this.editedFields.includes('offsite_location')) {
            return true
          }
          return false
        }
        if (this.editedFields.length > 0) {
          return true
        }
        return false
      },
      titleText() {
        switch (this.examType) {
          case 'group':
            return 'Group'
          case 'challenger':
            return 'Monthly Session'
          default:
            return 'Other'
        }
      },
      editedTimezone() {
        if (this.actionedExam && this.actionedExam.booking) {
          return this.actionedExam.booking.office.timezone.timezone_name
        }
        return ''
      },
      examType() {
        if (this.actionedExam && this.actionedExam.exam_type) {
          let { exam_type } = this.actionedExam
          if (exam_type.exam_type_name === 'Monthly Session Exam') {
            return 'challenger'
          }
          if (exam_type.group_exam_ind) {
            return 'group'
          }
          if (exam_type.ita_ind) {
            return 'individual'
          }
          return 'other'
        }
        return ''
      },
      fieldDisabled() {
        if ((this.role_code !== 'GA' && !this.is_liaison_designate) && this.examType != 'other') {
          return true
        }
        return false
      },
      modalVisible: {
        get() {
          return this.showModal
        },
        set(e) {
          this.toggleEditGroupBookingModal(e)
        }
      },
    },
    methods: {
      ...mapActions(['getBookings', 'getExams', 'postBooking', 'putRequest']),
      ...mapMutations(['toggleEditGroupBookingModal']),
      cancel() {
        this.toggleEditGroupBookingModal(false)
        this.reset()
        this.resetExam()
      },
      formatDate(d) {
        return new moment(d).format('ddd, MMM DD, YYYY')
      },
      formatTime(d) {
        return new moment(d).format('h:mm a')
      },
      checkDate(e) {
        let date = new moment(this.itemCopy.booking.start_time)
        let event = new moment(e)
        if (event.isBefore(moment(), 'day')) {
          return
        }
        this.date = event
        this.showMessage = false
        if (!this.itemCopy.booking) {
          if (!this.editedFields.includes('date')) {
            this.editedFields.push('date')
          }
          return
        }
        let oldDate = date.format('DDMMYYYY').toString()
        let newDate = new moment(e).format('DDMMYYYY').toString()
        if (newDate === oldDate) {
          if (this.editedFields.includes('date')) {
            let i = this.editedFields.indexOf('date')
            this.editedFields.splice(i,1)
          }
        }
        if (newDate !== date) {
          if (!this.editedFields.includes('date')) {
            this.editedFields.push('date')
          }
        }
      },
      checkTime(e) {
        this.time = e
        this.showMessage = false
        if (!this.itemCopy.booking) {
          if (!this.editedFields.includes('time')) {
            this.editedFields.push('time')
          }
          return
        }
        let time = zone.tz(this.itemCopy.booking.start_time, this.editedTimezone).format('HH:mm').toString()
        let newTime = new moment(e).format('HH:mm').toString()
        if (newTime === time) {
          if (this.editedFields.includes('time')) {
            let i = this.editedFields.indexOf('time')
            this.editedFields.splice(i,1)
          }
        }
        if (newTime !== time) {
          if (!this.editedFields.includes('time')) {
            this.editedFields.push('time')
          }
        }
      },
      checkInput(e) {
        let { name } = e.target
        let { value } = e.target
        this.showMessage = false
        if (name === 'offsite_location') {
          if (value !== this.itemCopy[name]) {
            if (!this.editedFields.includes(e.target.name)) {
              this.editedFields.push(e.target.name)
            }
            return
          }
          if (value === this.itemCopy[name]) {
            if (this.editedFields.includes(e.target.name)) {
              let i = this.editedFields.indexOf(e.target.name)
              this.editedFields.splice(i, 1)
            }
            return
          }
        }
        if (name === 'invigilator_id') {
          if (!this.itemCopy.booking) {
            if (!this.editedFields.includes(name)) {
              this.editedFields.push(name)
            }
            return
          }
          if (value == '') {
            if (this.itemCopy.booking.sbc_staff_invigilated) {
              if (!this.editedFields.includes(name)) {
                this.editedFields.push(name)
              }
              return
            }
            if (this.itemCopy.booking.invigilator_id) {
              if (!this.editedFields.includes(name)) {
                this.editedFields.push(name)
              }
              return
            }
            if (!this.itemCopy.booking.invigiator_id) {
              if (this.editedFields.includes(e.target.name)) {
                let i = this.editedFields.indexOf(e.target.name)
                this.editedFields.splice(i, 1)
              }
            }
            this.invigiator_id = ''
            return
          }
        }
        value = parseInt(value)
        if (value !== this.itemCopy.booking[name]) {
          if (!this.editedFields.includes(e.target.name)) {
            this.editedFields.push(e.target.name)
          }
          this[e.target.name] = e.target.value
          return
        }
        if (value == this.itemCopy.booking[name]) {
          if (this.editedFields.includes(e.target.name)) {
            let i = this.editedFields.indexOf(e.target.name)
            this.editedFields.splice(i, 1)
          }
          this[e.target.name] = e.target.value
          return
        }
      },
      submit() {
        if (!this.actionedExam.booking || !this.actionedExam.booking.start_time) {
          let { exam_id } = this.actionedExam
          let date = new moment(this.date).format('YYYY-MM-DD').toString()
          let time = new moment(this.time).format('HH:mm:ssZ').toString()
          let start = new moment(`${date}T${time}`)
          let end = start.clone().add(parseInt(this.actionedExam.exam_type.number_of_hours), 'h')
          let bookingPost = {
            exam_id,
            invigilator_id: null,
            sbc_staff_invigilated: false,
            start_time: start.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
            end_time: end.clone().utc().format('YYYY-MM-DD[T]HH:mm:ssZ'),
            booking_name: this.actionedExam.exam_name,
          }
          if (this.invigilator_id) {
            bookingPost.invigilator_id = this.invigilator_id
            if (this.invigilator_id === 'sbc') {
              bookingPost.sbc_staff_invigilated = true
              bookingPost.invigilator_id = null
            }
          }
          let examPut = {
            offsite_location: this.offsite_location
          }
          this.postBooking(bookingPost).then( booking_id => {
            examPut.booking_id = booking_id
            this.putRequest({url: `/exams/${exam_id}/`, data: examPut}).then( () => {
              this.getBookings().then( () => {
                this.getExams().then( () => {
                  this.cancel()
                })
              })
            })
          })
          return
        }
        let edits = this.editedFields
        let putRequests = []
        let local_timezone_name = this.user.office.timezone.timezone_name
        let edit_timezone_name = this.actionedExam.booking.office.timezone.timezone_name
        let bookingChanges = {}
        if (edits.includes('time') || edits.includes('date') || edits.includes('invigilator_id')
          || edits.includes('shadow_invigilator')) {
          let baseDate = moment(this.date).clone().format('YYYY-MM-DD')
          let baseTime = moment(this.time).clone().format('HH:mm:ss')
          let start
          if (local_timezone_name !== edit_timezone_name) {
            start =  zone.tz(`${baseDate}T${baseTime}`, edit_timezone_name)
          }
          if (local_timezone_name === edit_timezone_name) {
            start = moment(`${baseDate}T${baseTime}`)
          }
          let end = start.clone().add(parseInt(this.itemCopy.exam_type.number_of_hours), 'h')
          bookingChanges['start_time'] = start.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['end_time'] = end.utc().format('YYYY-MM-DD[T]HH:mm:ssZ')
          bookingChanges['invigilator_id'] = null
          bookingChanges['sbc_staff_invigilated'] = false
          if (this.invigilator_id) {
            if (this.invigilator_id === 'sbc') {
              bookingChanges.sbc_staff_invigilated = true
            } else {
              bookingChanges.invigilator_id = this.invigilator_id
              bookingChanges.sbc_staff_invigilated = false
            }
          }
          bookingChanges['shadow_invigilator_id'] = this.shadowInvigilator
          putRequests.push({url:`/bookings/${this.itemCopy.booking.booking_id}/`, data: bookingChanges})
          if(this.removeFlag == true){
            putRequests.push({url:`/invigilator/${this.currentShadowInvigilator}/?add=False&subtract=True`})
            this.removeFlag = false
          }else if(this.removeFlag == false){
            putRequests.push({url:`/invigilator/${this.shadowInvigilator}/?add=True&subtract=False`})
          }
        }
        let examChanges = {}
        if (edits.includes('offsite_location')) {
          examChanges['offsite_location'] = this.offsite_location
          putRequests.push({url:`/exams/${this.itemCopy.exam_id}/`, data: examChanges})
        }
        let promises = []
        putRequests.forEach( put => {
          promises.push(this.putRequest(put))
        })
        Promise.all(promises).then( () => {
          this.getBookings().then( () => {
            this.getExams().then( () => {
              this.cancel()
            })
          })
        })
      },
      show() {
        this.removeState = true
        this.changeState = true
        this.selectedShadow = null
        this.removeFlag = false
        let tempItem = Object.assign({}, this.actionedExam)
        if (tempItem.booking && tempItem.booking.start_time) {
          let { start_time } = tempItem.booking
          let { timezone_name } = this.actionedExam.booking.office.timezone
          let time = zone.tz(start_time, timezone_name).clone().format('YYYY-MM-DD[T]HH:mm:ss').toString()
          this.time = moment(time).format('YYYY-MM-DD[T]HH:mm:ssZ').toString()
          this.date = zone.tz(start_time, timezone_name).clone().format('YYYY-MM-DD[T]HH:mm:ssZ').toString()
          if (tempItem.booking.sbc_staff_invigilated) {
            this.invigilator_id = 'sbc'
          } else {
            this.invigilator_id = tempItem.booking.invigilator_id
          }
          let currentID = this.currentShadowInvigilator = this.actionedExam.booking.shadow_invigilator_id || null
          let currentName = ''
          this.shadow_invigilator_options.forEach(function(element) {
            if(element['id'] == currentID){
              currentName = element['name']
            }
          })

          this.currentShadowInvigilatorName = currentName
        }
        this.offsite_location = tempItem.offsite_location === '_offsite' ? null : tempItem.offsite_location
        this.editedFields = []
        this.itemCopy = tempItem
      },
      reset() {
        this.time = null
        this.date = null
        this.offsite_location = null
        this.invigilator_id = null
        this.itemCopy = {}
        this.editedFields = []
      },
      rowSelectedShadow(shadows, e){
        this.message = ''
        this.selectedShadow = shadows

        if (this.actionedExam && this.actionedExam.booking) {
          if (this.actionedExam.booking.shadow_invigilator_id !== e) {
            if (!this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.push('shadow_invigilator')
            }
          } else if (this.actionedExam.booking.shadow_invigilator_id == e) {
            if (this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.splice(this.editedFields.indexOf('shadow_invigilator'), 1)
            }
          }
        }
        if(shadows[0] == null){
          this.shadowInvigilator = null
        }else{
          this.shadowInvigilator = shadows[0].id
        }
      },
      setChange(){
        this.changeState = !this.changeState
        return
      },
      setRemove(){
        this.removeState = !this.removeState
        return
      },
      setSelectedShadowNull(e){
        this.removeFlag = true

        if (this.actionedExam && this.actionedExam.booking) {
          if (this.actionedExam.booking.shadow_invigilator_id !== e) {
            if (!this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.push('shadow_invigilator')
            }
          } else if (this.actionedExam.booking.shadow_invigilator_id == e) {
            if (this.editedFields.includes('shadow_invigilator')) {
              this.editedFields.splice(this.editedFields.indexOf('shadow_invigilator'), 1)
            }
          }
        }

        this.shadowInvigilator = null
        this.submit()
      }
    },
  }
</script>

<style scoped>
  .id-grid-1st-col {
    margin-left: auto;
    margin-right: 20px;
  }
  .id-grid-1st-col {
    grid-column: 1 / span 2;
    margin-right: 20px;
  }
  .custom-disabled-fields {
    color: #525252 !important;
  }
</style>
