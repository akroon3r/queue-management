<template>
    <b-modal v-model="modal"
             hide-header
             size="md"
             modal-class="q-modal"
             body-class="q-modal"
             no-close-on-backdrop
             @shown="show">
      <template slot="modal-footer">
        <div class="d-flex flex-row-reverse">
          <b-button v-if="this.recurring_form_state === 'notes' || this.single_form_state === 'notes'"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="recurring-submit"
                    @click="submit">
            Submit
          </b-button>
          <b-button v-else
                    class="ml-2"
                    size="md"
                    id="disabled-submit"
                    disabled>
            Submit
          </b-button>
          <b-button v-if="this.single_form_state === 'event_information'"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="single-event-information-next"
                    @click="nextRoomSingleSelection">
            Next
          </b-button>
          <b-button v-else-if="this.single_form_state === 'room_selection' && this.room_id_list.length > 0"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="single-room-select-next"
                    @click="nextSingleNotes">
            Next
          </b-button>
          <b-button v-else-if="this.recurring_form_state === 'rule_generated'"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="generate-next"
                    @click="generateRule">
            Next
          </b-button>
          <b-button v-else-if="this.recurring_form_state === 'audit'"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="audit-next"
                    @click="nextRoomSelection">
            Next
          </b-button>
          <b-button v-else-if="this.recurring_form_state === 'room_selection' && this.room_id_list.length > 0"
                    variant="primary"
                    class="ml-2"
                    size="md"
                    id="room-select-enabled"
                    @click="nextNotes">
            Next
          </b-button>
          <b-button v-else-if="(this.recurring_form_state === 'room_selection' && this.room_id_list.length === 0) ||
                               (this.single_form_state === 'room_selection' && this.room_id_list.length === 0) ||
                               (this.recurring_form_state === 'notes')"
                    disabled
                    class="ml-2"
                    size="md"
                    id="room-select-disabled">
            Next
          </b-button>
          <b-button @click="cancel">
            Cancel
          </b-button>
        </div>
    </template>
    <span style="font-size:1.75rem;">Schedule Booking Blackout</span><br>
    <b-form>
      <b-collapse id="collapse-booking-event-selection">
        <b-card>
          <b-form-row class="mb-2">
            <label>Step 1: Select Event Type</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col class="w-50">
              <b-button variant="primary"
                        class="w-100"
                        v-b-toggle.collapse-single-booking
                        @click="setRecurring">
                Create Single Blackout
              </b-button>
            </b-col>
            <b-col class="w-50">
              <b-button variant="primary"
                        class="w-100"
                        @click="setSingle"
                        v-b-toggle.collapse-recurring-booking>
                Create Recurring Blackout
              </b-button>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-single-booking" class="mt-2 mb-2">
        <b-card>
          <b-form-row style="justify-content: center;">
            <h4>Single Event</h4>
          </b-form-row>
          <b-form-row class="mb-2">
            <label style="font-weight: bold;">Step 2: Event Information</label>
          </b-form-row>
          <b-form-row class="mb-2">
            <b-col cols="6">
              <label>Booking Name</label><br>
              <b-form-input v-model="this.blackout_name"
                            disabled/>
            </b-col>
            <b-col cols="6">
              <label>Contact Information (optional)</label>
              <b-form-input v-model="this.user_contact_info"/>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Date</label>
                <font-awesome-icon v-if="this.blackout_date !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="blackout_date"
                            id="appointment_blackout_date"
                            type="date"
                            lang="en"
                            class="w-100"
                            @change="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout Start Time</label>
                <font-awesome-icon v-if="this.start_time !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="start_time"
                            id="appointment_blackout_start_time"
                            :time-picker-options="{ start: '8:00', step: '00:30', end: '17:30' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select Start Time"
                            class="w-100"
                            type="time"
                            @change="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
            <b-col cols="6">
              <b-form-group>
                <label>Blackout End Time</label>
                <font-awesome-icon v-if="this.end_time !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="end_time"
                            id="appointment_blackout_end_time"
                            :time-picker-options="{ start: '8:30', step: '00:30', end: '18:00' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select End Time"
                            class="w-100"
                            type="time"
                            @change="checkSingleInput">
                </DatePicker>
              </b-form-group>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-recurring-booking" class="mt-2">
        <b-card class="mb-2">
          <b-form-group>
            <b-form-row style="justify-content: center;">
              <h4>Recurring Event</h4>
            </b-form-row>
            <b-form-row class="mb-2">
              <label>Step 2: Event Information</label>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Booking Name</label><br>
                <b-form-input v-model="this.blackout_name"
                              disabled/>
              </b-col>
              <b-col cols="6">
                <label>Contact Information (optional)</label>
                <b-form-input v-model="this.user_contact_info"/>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Blackout Start Time</label>
                <font-awesome-icon v-if="this.recurring_booking_start_time !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="recurring_booking_start_time"
                            id="recurring_blackout_start_time"
                            :time-picker-options="{ start: '8:00', step: '00:30', end: '17:30' }"
                            lang="en"
                            format="h:mm a"
                            autocomplete="off"
                            placeholder="Select Start Time"
                            class="w-100"
                            type="time"
                            @change="checkRecurringInput">
                </DatePicker>
              </b-col>
              <b-col cols="6">
                <label>Blackout End Time</label>
                <font-awesome-icon v-if="this.recurring_booking_end_time !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker v-model="recurring_booking_end_time"
                            id="recurring_blackout_end_time"
                            :time-picker-options="{ start: '8:30', step: '00:30', end: '18:00' }"
                            lang="en"
                            format="h:mm a"
                            autocomplette="off"
                            placeholder="Select End Time"
                            class="w-100"
                            type="time"
                            @change="checkRecurringInput">
                </DatePicker>
              </b-col>
            </b-form-row>
            <b-form-row class="mb-2">
              <b-col cols="6">
                <label>Blackout Start Date</label>
                <font-awesome-icon v-if="this.recurring_booking_start_date!== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker id="recurring_booking_start_date"
                            class="w-100"
                            lang="en"
                            v-model="recurring_booking_start_date"
                            placeholder="Select Start Date"
                            @change="checkRecurringInput">
                </DatePicker>
              </b-col>
              <b-col cols="6">
                <label>Blackout End Date</label>
                <font-awesome-icon v-if="this.recurring_booking_end_date !== ''"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <DatePicker id="recurring_booking_end_date"
                            class="w-100"
                            lang="en"
                            v-model="recurring_booking_end_date"
                            @change="checkRecurringInput">
                </DatePicker>
              </b-col>
            </b-form-row>
            <b-form-row>
              <b-form-group class="mt-0 mb-0">
                <label>Frequency</label>
                <font-awesome-icon v-if="this.selected_booking_frequency.length === 1"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <font-awesome-icon v-if="this.selected_booking_frequency.length > 1"
                                   icon='exclamation-triangle'
                                   style="fontSize: 1rem; color: #FFC32B;"/>
                <label v-if="this.selected_booking_frequency.length > 1">Select one frequency</label>
                <b-form-checkbox-group id="frequency-checkboxes"
                                       v-model="selected_booking_frequency"
                                       @input="checkRecurringInput">
                  <b-form-checkbox :value="yearly">Yearly</b-form-checkbox>
                  <b-form-checkbox :value="monthly">Monthly</b-form-checkbox>
                  <b-form-checkbox :value="weekly">Weekly</b-form-checkbox>
                  <b-form-checkbox :value="daily">Daily</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
            </b-form-row>
            <b-form-row>
              <b-form-group class="mt-2">
                <label>Select Weekdays</label>
                <font-awesome-icon v-if="this.selected_booking_weekdays.length >= 1"
                                   icon='check'
                                   style="fontSize: 1rem; color: green;"/>
                <b-form-checkbox-group id="weekday-checkboxes"
                                       v-model="selected_booking_weekdays"
                                       @input="checkRecurringInput">
                  <b-form-checkbox :value="monday">Mon.</b-form-checkbox>
                  <b-form-checkbox :value="tuesday">Tues.</b-form-checkbox>
                  <b-form-checkbox :value="wednesday">Wed.</b-form-checkbox>
                  <b-form-checkbox :value="thursday">Thurs.</b-form-checkbox>
                  <b-form-checkbox :value="friday">Fri.</b-form-checkbox>
                </b-form-checkbox-group>
              </b-form-group>
            </b-form-row>
            <b-form-row>
              <label stlye="font-weight: bold" class="mt-0">Number of Occurences (optional):</label>
              <span v-if="this.selected_booking_count !== ''">&nbsp; Limited to {{ this.selected_booking_count }} occurences.</span>
              <font-awesome-icon v-if="this.selected_booking_count !== '' "
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"
                                 class="ml-1"/>
            </b-form-row>
            <b-form-row>
              <b-form-input type="number"
                            class="mb-1 w-25"
                            v-model="selected_booking_count">
              </b-form-input>
            </b-form-row>
          </b-form-group>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-information-audit">
        <b-card class="mb-2">
          <b-form-row style="justify-content: center;">
            <h4>Recurring Event</h4>
          </b-form-row>
          <b-form-row>
            <label style="font-weight: bold;">Step 2 (continued): Confirm Recurring Event Information</label>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.recurring-rule-collapse>
                View Recurring Event Info
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row class="mb-0">
            <b-collapse id="recurring-rule-collapse"
                        class="mb-2 ml-2"
                        visible>
              {{ this.booking_rrule_text }}
            </b-collapse>
          </b-form-row>
          <b-form-row>
            <b-col cols="12">
              <b-button variant="primary"
                        class="w-100 mb-2"
                        v-b-toggle.recurring-dates-collapse>
                View Recurring Dates ({{ this.booking_rrule_array.length }})
              </b-button>
            </b-col>
          </b-form-row>
          <b-form-row>
            <b-collapse id="recurring-dates-collapse"
                        class="mb-2">
              <div style="height: 75px; overflow-y: scroll; margin: 0px;">
                <ul class="list-group mb-0"
                    v-for="date in this.booking_rrule_array"
                    style="justify-content: center;">
                  <li class="list-group-item">
                    <b>Event:</b> {{ formatStartDate(date.start) }} until {{ formatEndDate(date.end) }}
                  </li>
                </ul>
              </div>
            </b-collapse>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-room-selection">
        <b-card>
          <b-form-row style="justify-content: center;">
            <h4 v-if="this.recurring_form_state === 'room_selection'">Recurring Event</h4>
            <h4 v-if="this.single_form_state === 'room_selection'">Single Event</h4>
          </b-form-row>
          <b-form-row>
            <label v-if="this.recurring_form_state === 'room_selection'"
                   style="font-weight: bold;">
              Step 3: Room Selection
            </label>
            <label v-if="this.single_form_state === 'room_selection'"
                   style="font-weight: bold;">
              Step 2: Room Selection
            </label>
          </b-form-row>
          <b-form-row class="mb-1">
            <b-col class="mr-2">
              <label>Select Room(s)</label>
              <b-table selectable
                      select-mode="multi"
                      selected-variant="success"
                      responsive
                      :fields="room_fields"
                      :items="this.roomResources"
                      style="height: 100px;"
                      bordered
                      striped
                      @row-selected="onRowSelected">
                <template slot="selected" slot-scope="{ rowSelected }">
                  <template v-if="rowSelected">
                    <span aria-hidden="true">&check;</span>
                    <span class="sr-only"Selected></span>
                  </template>
                  <template v-else>
                    <span aria-hidden="true">&nbsp;</span>
                    <span class="sr-only">Not selected</span>
                  </template>
                </template>
              </b-table>
            </b-col>
            <b-col>
              <b-row>
                <label>Selected Room(s)</label>
              </b-row>
              <b-row v-for="room in selected"
                     style="justify-content: center;">
                {{ room.name }}
              </b-row>
              <b-row v-if="this.room_id_list.length === 0"
                     style="justify-content: center;">
                <font-awesome-icon icon="exclamation-triangle"
                                   style="font-size: 3.0rem; color: #FFC32B;"
                                   class="p-1"/>
              </b-row>
              <b-row v-if="this.room_id_list.length > 0"
                     style="justify-content: center;">
                <font-awesome-icon icon="check"
                                   style="font-size: 3.0rem; color: green;"
                                   class="p-1"/>
              </b-row>
            </b-col>
          </b-form-row>
        </b-card>
      </b-collapse>
      <b-collapse id="collapse-booking-notes">
        <b-card>
          <b-form-row style="justify-content: center;">
            <h4 v-if="this.recurring_form_state === 'notes'">Recurring Event</h4>
            <h4 v-if="this.single_form_state === 'notes'">Single Event</h4>
          </b-form-row>
          <b-form-row>
            <b-form-group class="ml-1" style="width: 465px;">
              <label v-if="this.single_form_state === 'notes'">Step 3: Blackout Notes (optional)</label>
              <label v-if="this.recurring_form_state === 'notes'">Step 4: Blackout Notes (optional)</label>
              <font-awesome-icon v-if="this.notes !== ''"
                                 icon='check'
                                 style="fontSize: 1rem; color: green;"/>
              <b-textarea v-model="notes"
                          id="appointment_blackout_notes"
                          placeholder="Enter notes about blackout period"
                          rows="3"
                          max-rows="6"
                          size="md">
              </b-textarea>
            </b-form-group>
          </b-form-row>
        </b-card>
      </b-collapse>
    </b-form>
    </b-modal>
</template>

<script>
    import { mapActions, mapMutations, mapState } from 'vuex'
    import DatePicker from 'vue2-datepicker'
    import moment from 'moment'
    import { RRule } from 'rrule'

    export default {
      name: "BookingBlackoutModal",
      components: { DatePicker},
      created(){
        this.blackout_name = "BLACKOUT PERIOD"
        this.user_contact_info = this.$store.state.user.username
      },
      data(){
        return {
          blackout_date: '',
          start_time: '',
          end_time: '',
          notes: '',
          blackout_name: '',
          user_contact_info: '',
          selected: [],
          selectedLength: 0,
          room_id_list: [],
          room_fields: ['selected', 'title'],
          single_booking_blackout_boolean: true,
          recurring_booking_blackout_boolean: true,
          selected_booking_frequency: [],
          selected_booking_weekdays: [],
          selected_booking_count: '',
          recurring_booking_start_time: '',
          recurring_booking_end_time: '',
          recurring_booking_start_date: '',
          recurring_booking_end_date: '',
          yearly: RRule.YEARLY,
          monthly: RRule.MONTHLY,
          weekly: RRule.WEEKLY,
          daily: RRule.DAILY,
          monday: RRule.MO,
          tuesday: RRule.TU,
          wednesday: RRule.WE,
          thursday: RRule.TH,
          friday: RRule.FR,
          booking_rrule_array: [],
          booking_rrule_text: '',
          single_input_boolean: false,
          recurring_input_boolean: false,
          recurring_form_state: '',
          single_form_state: ''
        }
      },
      methods: {
        ...mapActions([
          'getBookings',
          'postBooking',
          'finishBooking',
        ]),
        ...mapMutations([
          'toggleBookingBlackoutModal'
        ]),
        hideCollapse(div_id){
          if(document.getElementById(div_id)){
            if(document.getElementById(div_id).classList.contains('show')){
              this.$root.$emit('bv::toggle::collapse', div_id)
            }
          }
        },
        showCollapse(div_id){
          if(document.getElementById(div_id)){
            if(document.getElementById(div_id).style.display === 'none'){
              this.$root.$emit('bv::toggle::collapse', div_id)
            }
          }
        },
        show(){
          this.showCollapse('collapse-booking-event-selection')
          this.showCollapse('collapse-single-booking')
          this.start_time = ''
          this.end_time = ''
          this.blackout_date = ''
          this.notes = ''
        },
        cancel(){
          this.toggleBookingBlackoutModal(false)
        },
        onRowSelected(roomResources){

          let roomResourceLength = roomResources.length
          let roomResourceIndex = roomResources.length - 1

          if (roomResourceIndex == -1) {
            roomResourceIndex = 0
          }

          if(this.selectedLength <= roomResourceLength){
            if(roomResourceLength == 1){
              this.selected.push({id: roomResources[0].id, name: roomResources[0].title})
              this.selectedLength = this.selected.length
              this.room_id_list.push(roomResources[0].id)
            }else if(roomResourceLength > 1){
              this.selected.push({id: roomResources[roomResourceIndex].id, name: roomResources[roomResourceIndex].title})
              this.selectedLength = this.selected.length
              this.room_id_list.push(roomResources[roomResourceIndex].id)
            }
          }else if(this.selectedLength > roomResourceLength){
            let remainingIDs = []
            roomResources.forEach(function(room) {
              remainingIDs.push(room.id)
            })
            let selectedIDs = []
            this.selected.forEach(function(room) {
              selectedIDs.push(room.id)
            })
            let difference  = selectedIDs.filter(x =>  !remainingIDs.includes(x))
            let indexOfDifference = this.selected.findIndex(x => x.id == difference)
            if(indexOfDifference !== undefined){
              this.selected.splice(indexOfDifference, 1)
            }
            let indexOfDifferenceRoomList = this.room_id_list.findIndex(x => x.id == difference)
            if(indexOfDifferenceRoomList !== undefined){
              this.room_id_list.splice(indexOfDifferenceRoomList, 1)
            }
          }
        },
        formatStartDate(date){
          let formatted_start_date = moment(date).format('YYYY-MM-DD HH:mm')
          return formatted_start_date
        },
        formatEndDate(date){
          let formatted_end_date = moment(date).format('YYYY-MM-DD HH:mm')
          return formatted_end_date
        },
        submit(e){
          e.preventDefault()
          let date = moment(this.blackout_date).clone().format('YYYY-MM-DD')
          let start = moment(this.start_time).clone().format('HH:mm:ss')
          let start_date = moment(date + " " + start).format()
          let end = moment(this.end_time).clone().format('HH:mm:ss')
          let end_date = moment(date + " " + end).format()

          if(this.booking_rrule_array.length === 0){
            if(this.room_id_list.length === 1){
              let blackout_booking = {}
              if(this.selected[0].id === '_offsite'){
                blackout_booking.start_time = start_date
                blackout_booking.end_time = end_date
                blackout_booking.booking_name = this.blackout_name
                blackout_booking.booking_contact_information = this.user_contact_info
                blackout_booking.blackout_flag = 'Y'
                blackout_booking.blackout_notes = this.notes
              }else {
                blackout_booking.start_time = start_date
                blackout_booking.end_time = end_date
                blackout_booking.booking_name = this.blackout_name
                blackout_booking.booking_contact_information = this.user_contact_info
                blackout_booking.room_id  = this.selected[0].id
                blackout_booking.blackout_flag = 'Y'
                blackout_booking.blackout_notes = this.notes
              }
              this.postBooking(blackout_booking).then( () => {
                this.finishBooking()
                this.toggleBookingBlackoutModal(false)
              })
              this.getBookings
            }else if(this.room_id_list.length > 1){
              let self = this
              this.room_id_list.forEach(function (room) {
                let blackout_booking = {}
                if(room == '_offsite'){
                  blackout_booking.start_time = start_date
                  blackout_booking.end_time = end_date
                  blackout_booking.booking_name = self.blackout_name
                  blackout_booking.booking_contact_information = self.user_contact_info
                  blackout_booking.blackout_flag = 'Y'
                  blackout_booking.blackout_notes = self.notes
                }else {
                  blackout_booking.start_time = start_date
                  blackout_booking.end_time = end_date
                  blackout_booking.booking_name = self.blackout_name
                  blackout_booking.booking_contact_information = self.user_contact_info
                  blackout_booking.room_id  = room
                  blackout_booking.blackout_flag = 'Y'
                  blackout_booking.blackout_notes = self.notes
                }
                self.postBooking(blackout_booking).then( () => {
                  self.getBookings()
                  self.toggleBookingBlackoutModal(false)
                })
              })
            }
          }else if(this.booking_rrule_array.length > 0){
            let booking_array = []
            let self = this
            if(this.room_id_list.length === 1){
              if(this.selected[0].id === '_offsite'){
                this.booking_rrule_array.forEach(date => {
                  let booking = {}
                  booking.start_time = date.start
                  booking.end_time = date.end
                  booking.booking_name = self.blackout_name
                  booking.booking_contact_information = self.user_contact_info
                  booking.blackout_flag = 'Y'
                  booking.blackout_notes = self.notes
                  booking_array.push(booking)
                })
              }else{
                this.booking_rrule_array.forEach(date => {
                  let booking = {}
                  booking.start_time = date.start
                  booking.end_time = date.end
                  booking.booking_name = self.blackout_name
                  booking.booking_contact_information = self.user_contact_info
                  booking.blackout_flag = 'Y'
                  booking.blackout_notes = self.notes
                  booking.room_id = self.selected[0].id
                  booking_array.push(booking)
                })
              }
            }else if(this.room_id_list.length > 1){
              this.room_id_list.forEach(room => {
                this.booking_rrule_array.forEach(date => {
                  let booking = {}
                  booking.room_id = room
                  booking.start_time = date.start
                  booking.end_time = date.end
                  booking.booking_name = self.blackout_name
                  booking.booking_contact_information = self.user_contact_info
                  booking.blackout_flag = 'Y'
                  booking.blackout_notes = self.notes

                  if(booking.room_id === '_offsite'){
                    delete booking.room_id
                  }

                  booking_array.push(booking)
                })
              })
            }
            booking_array.forEach(booking => {
              this.postBooking(booking)
              this.getBookings()
            })
            this.toggleBookingBlackoutModal(false)
          }
        },
        generateRule(){
          this.hideCollapse('collapse-booking-event-selection')
          this.hideCollapse('collapse-recurring-booking')
          this.single_booking_blackout_boolean = true
          this.recurring_booking_blackout_boolean = true
          let start_year = parseInt(moment(this.recurring_booking_start_date).clone().format('YYYY'))
          let start_month = parseInt(moment(this.recurring_booking_start_date).clone().format('MM'))
          let start_day = parseInt(moment(this.recurring_booking_start_date).clone().format('DD'))
          let start_hour = parseInt(moment(this.recurring_booking_start_time).clone().format('HH'))
          let start_minute = parseInt(moment(this.recurring_booking_start_time).clone().format('mm'))
          let end_year = parseInt(moment(this.recurring_booking_end_date).clone().format('YYYY'))
          let end_month = parseInt(moment(this.recurring_booking_end_date).clone().format('MM'))
          let end_day = parseInt(moment(this.recurring_booking_end_date).clone().format('DD'))
          let end_hour = parseInt(moment(this.recurring_booking_end_time).clone().format('HH'))
          let end_minute = parseInt(moment(this.recurring_booking_end_time).clone().format('mm'))
          let booking_input_frequency = null
          let local_booking_dates_array = []

          switch(this.selected_booking_frequency[0]){
            case 0:
              booking_input_frequency = RRule.YEARLY;
              break;
            case 1:
              booking_input_frequency = RRule.MONTHLY;
              break;
            case 2:
              booking_input_frequency = RRule.WEEKLY;
              break;
            case 3:
              booking_input_frequency = RRule.DAILY;
              break;
          }

          if(isNaN(start_year) == false || isNaN(end_year) == false){

            let date_start = new Date(Date.UTC(start_year, start_month-1, start_day, start_hour, start_minute))
            let until = new Date(Date.UTC(end_year, end_month-1, end_day, end_hour, end_minute))

            const rule = new RRule({
              freq: booking_input_frequency,
              count: this.selected_booking_count,
              byweekday: this.selected_booking_weekdays,
              dtstart: date_start,
              until: until,
            })

            let array = rule.all()
            this.booking_rrule_text = rule.toText()

            array.forEach(date => {
              let formatted_start_date = moment(date).clone().format('YYYY-MM-DD HH:mm:ssZ')
              let end_year = parseInt(moment(date).clone().format('YYYY'))
              let end_month = parseInt(moment(date).clone().format('MM'))
              let end_day = parseInt(moment(date).clone().format('DD'))
              let local_end_hour = end_hour
              let local_end_minute = end_minute
              let end = new Date(Date.UTC(end_year, end_month - 1, end_day, local_end_hour, local_end_minute))
              let end_moment = moment(end).clone().format('YYYY-MM-DD HH:mm:ssZ')
              let start_utc = moment.utc(formatted_start_date).clone().format('YYYY-MM-DD HH:mm:ssZ')
              let end_utc = moment.utc(end_moment).clone().format('YYYY-MM-DD HH:mm:ssZ')
              let start_utc_corrected = moment(start_utc).add(7, 'hours').format('YYYY-MM-DD HH:mm:ssZ')
              let end_utc_corrected = moment(end_utc).add(7, 'hours').format('YYYY-MM-DD HH:mm:ssZ')
              local_booking_dates_array.push({start: start_utc_corrected, end: end_utc_corrected})
            })
          }
          this.booking_rrule_array = local_booking_dates_array
          this.selected_booking_count = ''
          this.selected_booking_frequency = []
          this.selected_booking_weekdays = []
          this.recurring_booking_start_date = ''
          this.recurring_booking_start_time = ''
          this.recurring_booking_end_date = ''
          this.recurring_booking_end_time = ''
          this.recurring_form_state = 'audit'
          this.showCollapse('collapse-information-audit')
        },
        setSingle(){
          this.single_booking_blackout_boolean = !this.single_booking_blackout_boolean
          this.single_input_boolean = false
          this.blackout_date = ''
          this.start_time = ''
          this.end_time = ''
          this.recurring_form_state = ''
          this.single_form_state = ''
          this.hideCollapse('collapse-single-booking')
        },
        setRecurring(){
          this.recurring_booking_blackout_boolean = !this.recurring_booking_blackout_boolean
          this.single_input_boolean = false
          this.selected_booking_count = ''
          this.selected_booking_frequency = []
          this.selected_booking_weekdays = []
          this.recurring_booking_start_date = ''
          this.recurring_booking_start_time = ''
          this.recurring_booking_end_date = ''
          this.recurring_booking_end_time = ''
          this.recurring_form_state = ''
          this.single_form_state = ''
          this.hideCollapse('collapse-recurring-booking')
        },
        checkSingleInput(){
          if(this.blackout_date !== '' && this.start_time !== '' && this.end_time !== ''){
            this.single_input_boolean = true
            this.single_form_state = 'event_information'
          }
        },
        checkRecurringInput(){
          if(this.selected_booking_frequency.length > 0 && this.recurring_booking_start_date !== ''
            && this.recurring_booking_start_time !== '' && this.recurring_booking_end_date !== ''
            && this.recurring_booking_end_time !== ''){
            this.recurring_input_boolean = true
            this.recurring_form_state = 'rule_generated'
          }
        },
        nextRoomSingleSelection(){
          this.hideCollapse('collapse-single-booking')
          this.hideCollapse('collapse-booking-event-selection')
          this.showCollapse('collapse-room-selection')
          this.single_form_state = 'room_selection'
        },
        nextRoomSelection(){
          this.hideCollapse('collapse-information-audit')
          this.showCollapse('collapse-room-selection')
          this.hideCollapse('collapse-booking-event-selection')
          this.recurring_form_state = 'room_selection'
        },
        nextSingleNotes(){
          this.hideCollapse('collapse-room-selection')
          this.showCollapse('collapse-booking-notes')
          this.single_form_state = 'notes'
        },
        nextNotes(){
          this.hideCollapse('collapse-room-selection')
          this.showCollapse('collapse-booking-notes')
          this.recurring_form_state = 'notes'
        },
      },
      computed: {
        ...mapState({
          showBookingBlackoutModal: state => state.showBookingBlackoutModal,
          rooms: state => state.rooms,
          roomResources: state => state.roomResources,
        }),
        modal: {
          get() {
            return this.showBookingBlackoutModal
          },
          set(e) {
            this.toggleBookingBlackoutModal(e)
            let all_rooms_local = []
            this.roomResources.forEach(function(room){
              all_rooms_local.push(room.title)
            })
          }
        },
      }
    }
</script>


<style scoped>

</style>
